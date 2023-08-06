use std::{
    cell::RefCell,
    ops::{Deref, DerefMut},
};

use ahash::{HashMap, HashMapExt};
use smartstring::alias::String;

use crate::{
    representations::{Atom, Identifier, OwnedAtom},
    rings::finite_field::{FiniteField, FiniteFieldCore},
};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FiniteFieldIndex(pub(crate) usize);

pub(crate) const INPUT_ID: Identifier = Identifier::init(u32::MAX);

/// A global state, that stores mappings from variable and function names to ids.
#[derive(Clone)]
pub struct State {
    // get variable maps from here
    str_to_var_id: HashMap<String, Identifier>,
    var_to_str_map: Vec<String>,
    finite_fields: Vec<FiniteField<u64>>,
}

impl State {
    pub fn new() -> State {
        State {
            str_to_var_id: HashMap::new(),
            var_to_str_map: vec![],
            finite_fields: vec![],
        }
    }

    // note: could be made immutable by using frozen collections
    /// Get the id for a certain name if the name is already registered,
    /// else register it and return a new id.
    pub fn get_or_insert_var<S: AsRef<str>>(&mut self, name: S) -> Identifier {
        match self.str_to_var_id.entry(name.as_ref().into()) {
            std::collections::hash_map::Entry::Occupied(o) => *o.get(),
            std::collections::hash_map::Entry::Vacant(v) => {
                if self.var_to_str_map.len() == u32::MAX as usize - 1 {
                    panic!("Too many variables defined");
                }

                let new_id = Identifier::from(self.var_to_str_map.len() as u32);
                v.insert(new_id);
                self.var_to_str_map.push(name.as_ref().into());
                new_id
            }
        }
    }

    /// Get the name for a given id.
    pub fn get_name(&self, id: Identifier) -> Option<&String> {
        self.var_to_str_map.get(id.to_u32() as usize)
    }

    pub fn is_wildcard(&self, id: Identifier) -> Option<bool> {
        self.get_name(id).map(|n| n.ends_with('_'))
    }

    pub fn get_finite_field(&self, fi: FiniteFieldIndex) -> &FiniteField<u64> {
        &self.finite_fields[fi.0]
    }

    pub fn get_or_insert_finite_field(&mut self, f: FiniteField<u64>) -> FiniteFieldIndex {
        for (i, f2) in self.finite_fields.iter().enumerate() {
            if f.get_prime() == f2.get_prime() {
                return FiniteFieldIndex(i);
            }
        }

        self.finite_fields.push(f);
        FiniteFieldIndex(self.finite_fields.len() - 1)
    }
}

/// A workspace that stores reusable buffers.
pub struct Workspace<P: Atom> {
    atom_stack: Stack<OwnedAtom<P>>,
}

impl<P: Atom> Workspace<P> {
    pub fn new() -> Workspace<P> {
        Workspace {
            atom_stack: Stack::new(),
        }
    }

    pub fn new_atom(&self) -> BufferHandle<OwnedAtom<P>> {
        self.atom_stack.get_buf_ref()
    }
}

/// A buffer that can be reset to its initial state.
/// The `new` function may allocate, but the `reset` function must not.
pub trait ResettableBuffer: Sized {
    /// Create a new resettable buffer. May allocate.
    fn new() -> Self;
    /// Reset the buffer to its initial state. Must not allocate.
    fn reset(&mut self);
}

/// A stack of resettable buffers. Any buffer lend from this stack
/// will be returned to it when it is dropped. If a buffer is requested
/// on an empty stack, a new buffer will be created. Use a stack to prevent
/// allocations by recycling used buffers first before creating new ones.
pub struct Stack<T: ResettableBuffer> {
    buffers: RefCell<Vec<T>>,
}

impl<T: ResettableBuffer> Stack<T> {
    /// Create a new stack.
    #[inline]
    pub fn new() -> Self {
        Self {
            buffers: RefCell::new(vec![]),
        }
    }

    /// Get a buffer from the stack if the stack is not empty,
    /// else create a new one.
    #[inline]
    pub fn get_buf_ref(&self) -> BufferHandle<T> {
        let b = self
            .buffers
            .borrow_mut()
            .pop()
            .map(|mut b| {
                b.reset();
                b
            })
            .unwrap_or_else(|| T::new());

        BufferHandle {
            buf: Some(b),
            parent: self,
        }
    }

    /// Return a buffer to the stack.
    #[inline]
    fn return_arg(&self, b: T) {
        self.buffers.borrow_mut().push(b);
    }
}

/// A handle to an underlying resettable buffer. When this handle is dropped,
/// the buffer is returned to the stack it was created by.
pub struct BufferHandle<'a, T: ResettableBuffer> {
    buf: Option<T>,
    parent: &'a Stack<T>,
}

impl<'a, T: ResettableBuffer> Deref for BufferHandle<'a, T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        self.get()
    }
}

impl<'a, T: ResettableBuffer> DerefMut for BufferHandle<'a, T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        self.get_mut()
    }
}

impl<'a, T: ResettableBuffer> BufferHandle<'a, T> {
    /// Get an immutable reference to the underlying buffer.
    #[inline]
    pub fn get(&self) -> &T {
        self.buf.as_ref().unwrap()
    }

    /// Get a mutable reference to the underlying buffer.
    #[inline]
    pub fn get_mut(&mut self) -> &mut T {
        self.buf.as_mut().unwrap()
    }
}

impl<'a, T: ResettableBuffer> Drop for BufferHandle<'a, T> {
    /// Upon dropping the handle, the buffer is returned to the stack it was created by.
    #[inline]
    fn drop(&mut self) {
        self.parent
            .return_arg(std::mem::take(&mut self.buf).unwrap())
    }
}
