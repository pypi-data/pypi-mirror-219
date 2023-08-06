use std::{
    borrow::{Borrow, BorrowMut},
    ops::Neg,
    sync::{Arc, RwLock},
};

use ahash::{HashMap, HashMapExt};
use once_cell::sync::Lazy;
use pyo3::{
    exceptions, pyclass,
    pyclass::CompareOp,
    pymethods, pymodule,
    types::{PyModule, PyTuple, PyType},
    FromPyObject, IntoPy, PyObject, PyRef, PyResult, Python,
};
use self_cell::self_cell;
use smallvec::SmallVec;

use crate::{
    id::{Match, MatchStack, Pattern, PatternAtomTreeIterator, PatternRestriction},
    parser::parse,
    poly::{polynomial::MultivariatePolynomial, INLINED_EXPONENTS},
    printer::{AtomPrinter, PolynomialPrinter, PrintMode, RationalPolynomialPrinter},
    representations::{
        default::{
            DefaultRepresentation, ListIteratorD, OwnedAddD, OwnedFunD, OwnedMulD, OwnedNumD,
            OwnedPowD, OwnedVarD,
        },
        number::{BorrowedNumber, Number},
        Add, AtomView, Fun, Identifier, Mul, Num, OwnedAdd, OwnedAtom, OwnedFun, OwnedMul,
        OwnedNum, OwnedPow, OwnedVar, Var,
    },
    rings::integer::IntegerRing,
    rings::{
        rational::RationalField,
        rational_polynomial::{FromNumeratorAndDenominator, RationalPolynomial},
    },
    state::{ResettableBuffer, State, Workspace, INPUT_ID},
    streaming::TermStreamer,
    transformer::Transformer,
};

static STATE: Lazy<RwLock<State>> = Lazy::new(|| RwLock::new(State::new()));
thread_local!(static WORKSPACE: Workspace<DefaultRepresentation> = Workspace::new());

#[pymodule]
fn symbolica(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PythonExpression>()?;
    m.add_class::<PythonFunction>()?;
    m.add_class::<PythonPattern>()?;
    m.add_class::<PythonPolynomial>()?;
    m.add_class::<PythonIntegerPolynomial>()?;
    m.add_class::<PythonRationalPolynomial>()?;
    m.add_class::<PythonRationalPolynomialSmallExponent>()?;

    Ok(())
}

#[derive(FromPyObject)]
pub enum ConvertibleToPattern {
    Literal(ConvertibleToExpression),
    Pattern(PythonPattern),
}

impl ConvertibleToPattern {
    pub fn to_pattern(self) -> PythonPattern {
        match self {
            Self::Literal(l) => PythonPattern {
                expr: Arc::new(Pattern::from_view(
                    l.to_expression().expr.to_view(),
                    &STATE.read().unwrap(),
                )),
            },
            Self::Pattern(e) => e,
        }
    }
}

#[pyclass(name = "Transformer")]
#[derive(Clone)]
pub struct PythonPattern {
    pub expr: Arc<Pattern<DefaultRepresentation>>,
}

#[pymethods]
impl PythonPattern {
    #[new]
    pub fn new() -> PythonPattern {
        PythonPattern {
            expr: Arc::new(Pattern::Transformer(Box::new(Transformer::Input))),
        }
    }

    pub fn expand(&self) -> PyResult<PythonPattern> {
        Ok(PythonPattern {
            expr: Arc::new(Pattern::Transformer(Box::new(Transformer::Expand(
                (*self.expr).clone(),
            )))),
        })
    }

    pub fn replace_all(
        &self,
        lhs: ConvertibleToPattern,
        rhs: ConvertibleToPattern,
        cond: Option<PythonPatternRestriction>,
    ) -> PyResult<PythonPattern> {
        Ok(PythonPattern {
            expr: Arc::new(Pattern::Transformer(Box::new(Transformer::ReplaceAll(
                (*lhs.to_pattern().expr).clone(),
                (*self.expr).clone(),
                (*rhs.to_pattern().expr).clone(),
                cond.map(|r| r.convert()).unwrap_or(HashMap::default()),
            )))),
        })
    }

    pub fn __add__(&self, rhs: ConvertibleToPattern) -> PythonPattern {
        let res = WORKSPACE.with(|workspace| {
            self.expr.add(
                &rhs.to_pattern().expr,
                workspace,
                STATE.read().unwrap().borrow(),
            )
        });

        PythonPattern {
            expr: Arc::new(res),
        }
    }

    pub fn __radd__(&self, rhs: ConvertibleToPattern) -> PythonPattern {
        self.__add__(rhs)
    }

    pub fn __sub__(&self, rhs: ConvertibleToPattern) -> PythonPattern {
        self.__add__(ConvertibleToPattern::Pattern(rhs.to_pattern().__neg__()))
    }

    pub fn __rsub__(&self, rhs: ConvertibleToPattern) -> PythonPattern {
        rhs.to_pattern()
            .__add__(ConvertibleToPattern::Pattern(self.__neg__()))
    }

    pub fn __mul__(&self, rhs: ConvertibleToPattern) -> PythonPattern {
        let res = WORKSPACE.with(|workspace| {
            self.expr.mul(
                &rhs.to_pattern().expr,
                workspace,
                STATE.read().unwrap().borrow(),
            )
        });

        PythonPattern {
            expr: Arc::new(res),
        }
    }

    pub fn __rmul__(&self, rhs: ConvertibleToPattern) -> PythonPattern {
        self.__mul__(rhs)
    }

    pub fn __truediv__(&self, rhs: ConvertibleToPattern) -> PythonPattern {
        let res = WORKSPACE.with(|workspace| {
            self.expr.div(
                &rhs.to_pattern().expr,
                workspace,
                STATE.read().unwrap().borrow(),
            )
        });

        PythonPattern {
            expr: Arc::new(res),
        }
    }

    pub fn __rtruediv__(&self, rhs: ConvertibleToPattern) -> PythonPattern {
        rhs.to_pattern()
            .__truediv__(ConvertibleToPattern::Pattern(self.clone()))
    }

    pub fn __pow__(
        &self,
        rhs: ConvertibleToPattern,
        number: Option<i64>,
    ) -> PyResult<PythonPattern> {
        if number.is_some() {
            return Err(exceptions::PyValueError::new_err(
                "Optional number argument not supported",
            ));
        }

        let res = WORKSPACE.with(|workspace| {
            self.expr.pow(
                &rhs.to_pattern().expr,
                workspace,
                STATE.read().unwrap().borrow(),
            )
        });

        Ok(PythonPattern {
            expr: Arc::new(res),
        })
    }

    pub fn __rpow__(
        &self,
        rhs: ConvertibleToPattern,
        number: Option<i64>,
    ) -> PyResult<PythonPattern> {
        rhs.to_pattern()
            .__pow__(ConvertibleToPattern::Pattern(self.clone()), number)
    }

    pub fn __xor__(&self, _rhs: PyObject) -> PyResult<PythonPattern> {
        Err(exceptions::PyTypeError::new_err(
            "Cannot xor an expression. Did you mean to write a power? Use ** instead, i.e. x**2",
        ))
    }

    pub fn __rxor__(&self, _rhs: PyObject) -> PyResult<PythonPattern> {
        Err(exceptions::PyTypeError::new_err(
            "Cannot xor an expression. Did you mean to write a power? Use ** instead, i.e. x**2",
        ))
    }

    pub fn __neg__(&self) -> PythonPattern {
        let res =
            WORKSPACE.with(|workspace| self.expr.neg(workspace, STATE.read().unwrap().borrow()));

        PythonPattern {
            expr: Arc::new(res),
        }
    }
}

#[pyclass(name = "Expression")]
#[derive(Clone)]
pub struct PythonExpression {
    pub expr: Arc<OwnedAtom<DefaultRepresentation>>,
}

/// A subset of pattern restrictions that can be used in Python.
#[derive(Debug, Clone, Copy)]
pub enum SimplePatternRestriction {
    Length(Identifier, usize, Option<usize>), // min-max range
    IsVar(Identifier),
    IsNumber(Identifier),
    IsLiteralWildcard(Identifier), // matches x_ to x_ only
    NumberCmp(Identifier, CompareOp, i64),
}

#[pyclass(name = "PatternRestriction")]
#[derive(Debug, Clone)]
pub struct PythonPatternRestriction {
    pub restrictions: Arc<Vec<SimplePatternRestriction>>,
}

impl PythonPatternRestriction {
    fn convert(&self) -> HashMap<Identifier, Vec<PatternRestriction<DefaultRepresentation>>> {
        let mut restrictions = HashMap::with_capacity(self.restrictions.len());

        for r in &*self.restrictions {
            match *r {
                SimplePatternRestriction::IsVar(name) => {
                    restrictions
                        .entry(name)
                        .or_insert(vec![])
                        .push(PatternRestriction::<DefaultRepresentation>::IsVar);
                }
                SimplePatternRestriction::IsLiteralWildcard(name) => {
                    restrictions
                        .entry(name)
                        .or_insert(vec![])
                        .push(PatternRestriction::<DefaultRepresentation>::IsLiteralWildcard(name));
                }
                SimplePatternRestriction::IsNumber(name) => {
                    restrictions
                        .entry(name)
                        .or_insert(vec![])
                        .push(PatternRestriction::IsNumber);
                }
                SimplePatternRestriction::Length(name, min, max) => {
                    restrictions
                        .entry(name)
                        .or_insert(vec![])
                        .push(PatternRestriction::Length(min, max));
                }
                SimplePatternRestriction::NumberCmp(name, op, ref_num) => {
                    restrictions
                        .entry(name)
                        .or_insert(vec![])
                        .push(PatternRestriction::Filter(Box::new(
                            move |v: &Match<DefaultRepresentation>| match v {
                                Match::Single(AtomView::Num(n)) => {
                                    let num = n.get_number_view();
                                    let ordering = num.cmp(&BorrowedNumber::Natural(ref_num, 1));
                                    match op {
                                        CompareOp::Lt => ordering.is_lt(),
                                        CompareOp::Le => ordering.is_le(),
                                        CompareOp::Eq => ordering.is_eq(),
                                        CompareOp::Ne => ordering.is_ne(),
                                        CompareOp::Gt => ordering.is_gt(),
                                        CompareOp::Ge => ordering.is_ge(),
                                    }
                                }
                                _ => false,
                            },
                        )));
                }
            }
        }

        restrictions
    }
}

#[pymethods]
impl PythonPatternRestriction {
    pub fn __and__(&self, other: Self) -> PythonPatternRestriction {
        PythonPatternRestriction {
            restrictions: Arc::new(
                self.restrictions
                    .iter()
                    .chain(other.restrictions.iter())
                    .cloned()
                    .collect(),
            ),
        }
    }
}

#[derive(FromPyObject)]
pub enum ConvertibleToExpression {
    Int(i64),
    Expression(PythonExpression),
}

impl ConvertibleToExpression {
    pub fn to_expression(self) -> PythonExpression {
        match self {
            ConvertibleToExpression::Int(i) => {
                let mut num = OwnedAtom::new();
                let num_d: &mut OwnedNumD = num.transform_to_num();
                num_d.set_from_number(Number::Natural(i, 1));
                PythonExpression {
                    expr: Arc::new(num),
                }
            }
            ConvertibleToExpression::Expression(e) => e,
        }
    }
}

#[pymethods]
impl PythonExpression {
    #[classmethod]
    pub fn var(_cls: &PyType, name: &str) -> PyResult<PythonExpression> {
        let mut guard = STATE.write().unwrap();
        let state = guard.borrow_mut();
        // TODO: check if the name meets the requirements
        let id = state.get_or_insert_var(name);
        let mut var = OwnedAtom::new();
        let o: &mut OwnedVarD = var.transform_to_var();
        o.set_from_id(id);

        Ok(PythonExpression {
            expr: Arc::new(var),
        })
    }

    #[pyo3(signature = (*args,))]
    #[classmethod]
    pub fn vars(_cls: &PyType, args: &PyTuple) -> PyResult<Vec<PythonExpression>> {
        let mut guard = STATE.write().unwrap();
        let state = guard.borrow_mut();
        let mut result = Vec::with_capacity(args.len());

        for a in args {
            // TODO: check if the name meets the requirements
            let name = a.extract::<&str>()?;
            let id = state.get_or_insert_var(name);
            let mut var = OwnedAtom::new();
            let o: &mut OwnedVarD = var.transform_to_var();
            o.set_from_id(id);

            result.push(PythonExpression {
                expr: Arc::new(var),
            });
        }

        Ok(result)
    }

    #[classmethod]
    pub fn fun(_cls: &PyType, name: &str) -> PyResult<PythonFunction> {
        PythonFunction::__new__(name)
    }

    #[pyo3(signature = (*args,))]
    #[classmethod]
    pub fn funs(_cls: &PyType, args: &PyTuple) -> PyResult<Vec<PythonFunction>> {
        let mut result = Vec::with_capacity(args.len());
        for a in args {
            let name = a.extract::<&str>()?;
            result.push(PythonFunction::__new__(name)?);
        }

        Ok(result)
    }

    #[classmethod]
    pub fn parse(_cls: &PyType, arg: &str) -> PyResult<PythonExpression> {
        let e = WORKSPACE.with(|f| {
            parse(arg)
                .map_err(exceptions::PyValueError::new_err)?
                .to_atom(STATE.write().unwrap().borrow_mut(), f)
                .map_err(exceptions::PyValueError::new_err)
        })?;

        Ok(PythonExpression { expr: Arc::new(e) })
    }

    pub fn __copy__(&self) -> PythonExpression {
        PythonExpression {
            expr: Arc::new((*self.expr).clone()),
        }
    }

    pub fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "{}",
            AtomPrinter {
                atom: self.expr.to_view(),
                state: &STATE.read().unwrap(),
                print_mode: PrintMode::default(),
            }
        ))
    }

    /// Create a wildcard from a variable name.
    ///
    #[getter]
    fn get_w(&self) -> PyResult<PythonExpression> {
        let mut guard = STATE.write().unwrap();
        let state = guard.borrow_mut();
        let mut var_name = match self.expr.to_view() {
            AtomView::Var(v) => {
                if let Some(true) = state.is_wildcard(v.get_name()) {
                    return Ok(self.clone());
                } else {
                    // create name with underscore
                    state.get_name(v.get_name()).unwrap().to_string()
                }
            }
            AtomView::Fun(f) => {
                if let Some(true) = state.is_wildcard(f.get_name()) {
                    return Ok(self.clone());
                } else {
                    // create name with underscore
                    state.get_name(f.get_name()).unwrap().to_string()
                }
            }
            x => {
                return Err(exceptions::PyValueError::new_err(format!(
                    "Cannot convert to wildcard: {:?}",
                    x
                )));
            }
        };

        // create name with underscore
        var_name.push('_');

        // TODO: check if the name meets the requirements
        let id = state.get_or_insert_var(var_name);
        let mut var = OwnedAtom::new();
        let o: &mut OwnedVarD = var.transform_to_var();
        o.set_from_id(id);

        Ok(PythonExpression {
            expr: Arc::new(var),
        })
    }

    pub fn __add__(&self, rhs: ConvertibleToExpression) -> PythonExpression {
        let b = WORKSPACE.with(|workspace| {
            let mut e = workspace.new_atom();
            let a: &mut OwnedAddD = e.transform_to_add();

            a.extend(self.expr.to_view());
            a.extend(rhs.to_expression().expr.to_view());
            a.set_dirty(true);

            let mut b = OwnedAtom::new();
            e.get()
                .to_view()
                .normalize(workspace, STATE.read().unwrap().borrow(), &mut b);
            b
        });

        PythonExpression { expr: Arc::new(b) }
    }

    pub fn __radd__(&self, rhs: ConvertibleToExpression) -> PythonExpression {
        self.__add__(rhs)
    }

    pub fn __sub__(&self, rhs: ConvertibleToExpression) -> PythonExpression {
        self.__add__(ConvertibleToExpression::Expression(
            rhs.to_expression().__neg__(),
        ))
    }

    pub fn __rsub__(&self, rhs: ConvertibleToExpression) -> PythonExpression {
        rhs.to_expression()
            .__add__(ConvertibleToExpression::Expression(self.__neg__()))
    }

    pub fn __mul__(&self, rhs: ConvertibleToExpression) -> PythonExpression {
        let b = WORKSPACE.with(|workspace| {
            let mut e = workspace.new_atom();
            let a: &mut OwnedMulD = e.transform_to_mul();

            a.extend(self.expr.to_view());
            a.extend(rhs.to_expression().expr.to_view());
            a.set_dirty(true);

            let mut b = OwnedAtom::new();
            e.get()
                .to_view()
                .normalize(workspace, STATE.read().unwrap().borrow(), &mut b);
            b
        });

        PythonExpression { expr: Arc::new(b) }
    }

    pub fn __rmul__(&self, rhs: ConvertibleToExpression) -> PythonExpression {
        self.__mul__(rhs)
    }

    pub fn __truediv__(&self, rhs: ConvertibleToExpression) -> PythonExpression {
        let b = WORKSPACE.with(|workspace| {
            let mut pow = workspace.new_atom();
            let pow_num = pow.transform_to_num();
            pow_num.set_from_number(Number::Natural(-1, 1));

            let mut e = workspace.new_atom();
            let a: &mut OwnedPowD = e.transform_to_pow();
            a.set_from_base_and_exp(rhs.to_expression().expr.to_view(), pow.get().to_view());
            a.set_dirty(true);

            let mut m = workspace.new_atom();
            let md: &mut OwnedMulD = m.transform_to_mul();

            md.extend(self.expr.to_view());
            md.extend(e.get().to_view());
            md.set_dirty(true);

            let mut b = OwnedAtom::new();
            m.get()
                .to_view()
                .normalize(workspace, STATE.read().unwrap().borrow(), &mut b);
            b
        });
        PythonExpression { expr: Arc::new(b) }
    }

    pub fn __rtruediv__(&self, rhs: ConvertibleToExpression) -> PythonExpression {
        rhs.to_expression()
            .__truediv__(ConvertibleToExpression::Expression(self.clone()))
    }

    pub fn __pow__(
        &self,
        rhs: ConvertibleToExpression,
        number: Option<i64>,
    ) -> PyResult<PythonExpression> {
        if number.is_some() {
            return Err(exceptions::PyValueError::new_err(
                "Optional number argument not supported",
            ));
        }

        let b = WORKSPACE.with(|workspace| {
            let mut e = workspace.new_atom();
            let a: &mut OwnedPowD = e.transform_to_pow();

            a.set_from_base_and_exp(self.expr.to_view(), rhs.to_expression().expr.to_view());
            a.set_dirty(true);

            let mut b = OwnedAtom::new();
            e.get()
                .to_view()
                .normalize(workspace, STATE.read().unwrap().borrow(), &mut b);
            b
        });

        Ok(PythonExpression { expr: Arc::new(b) })
    }

    pub fn __rpow__(
        &self,
        rhs: ConvertibleToExpression,
        number: Option<i64>,
    ) -> PyResult<PythonExpression> {
        rhs.to_expression()
            .__pow__(ConvertibleToExpression::Expression(self.clone()), number)
    }

    pub fn __xor__(&self, _rhs: PyObject) -> PyResult<PythonExpression> {
        Err(exceptions::PyTypeError::new_err(
            "Cannot xor an expression. Did you mean to write a power? Use ** instead, i.e. x**2",
        ))
    }

    pub fn __rxor__(&self, _rhs: PyObject) -> PyResult<PythonExpression> {
        Err(exceptions::PyTypeError::new_err(
            "Cannot xor an expression. Did you mean to write a power? Use ** instead, i.e. x**2",
        ))
    }

    pub fn __neg__(&self) -> PythonExpression {
        let b = WORKSPACE.with(|workspace| {
            let mut e = workspace.new_atom();
            let a: &mut OwnedMulD = e.transform_to_mul();

            let mut sign = workspace.new_atom();
            let sign_num = sign.transform_to_num();
            sign_num.set_from_number(Number::Natural(-1, 1));

            a.extend(self.expr.to_view());
            a.extend(sign.get().to_view());
            a.set_dirty(true);

            let mut b = OwnedAtom::new();
            e.get()
                .to_view()
                .normalize(workspace, STATE.read().unwrap().borrow(), &mut b);
            b
        });

        PythonExpression { expr: Arc::new(b) }
    }

    fn __len__(&self) -> usize {
        match self.expr.to_view() {
            AtomView::Add(a) => a.get_nargs(),
            AtomView::Mul(a) => a.get_nargs(),
            AtomView::Fun(a) => a.get_nargs(),
            _ => 1,
        }
    }

    pub fn transform(&self) -> PythonPattern {
        PythonPattern {
            expr: Arc::new(Pattern::Literal((*self.expr).clone())),
        }
    }

    /// Create a pattern restriction based on the length.
    pub fn len(
        &self,
        min_length: usize,
        max_length: Option<usize>,
    ) -> PyResult<PythonPatternRestriction> {
        match self.expr.to_view() {
            AtomView::Var(v) => {
                let name = v.get_name();
                if !STATE.read().unwrap().is_wildcard(name).unwrap_or(false) {
                    return Err(exceptions::PyTypeError::new_err(
                        "Only wildcards can be restricted.",
                    ));
                }

                Ok(PythonPatternRestriction {
                    restrictions: Arc::new(vec![SimplePatternRestriction::Length(
                        name, min_length, max_length,
                    )]),
                })
            }
            _ => Err(exceptions::PyTypeError::new_err(
                "Only wildcards can be restricted.",
            )),
        }
    }

    pub fn is_var(&self) -> PyResult<PythonPatternRestriction> {
        match self.expr.to_view() {
            AtomView::Var(v) => {
                let name = v.get_name();
                if !STATE.read().unwrap().is_wildcard(name).unwrap_or(false) {
                    return Err(exceptions::PyTypeError::new_err(
                        "Only wildcards can be restricted.",
                    ));
                }

                Ok(PythonPatternRestriction {
                    restrictions: Arc::new(vec![SimplePatternRestriction::IsVar(name)]),
                })
            }
            _ => Err(exceptions::PyTypeError::new_err(
                "Only wildcards can be restricted.",
            )),
        }
    }

    pub fn is_num(&self) -> PyResult<PythonPatternRestriction> {
        match self.expr.to_view() {
            AtomView::Var(v) => {
                let name = v.get_name();
                if !STATE.read().unwrap().is_wildcard(name).unwrap_or(false) {
                    return Err(exceptions::PyTypeError::new_err(
                        "Only wildcards can be restricted.",
                    ));
                }

                Ok(PythonPatternRestriction {
                    restrictions: Arc::new(vec![SimplePatternRestriction::IsNumber(name)]),
                })
            }
            _ => Err(exceptions::PyTypeError::new_err(
                "Only wildcards can be restricted.",
            )),
        }
    }

    pub fn is_lit(&self) -> PyResult<PythonPatternRestriction> {
        match self.expr.to_view() {
            AtomView::Var(v) => {
                let name = v.get_name();
                if !STATE.read().unwrap().is_wildcard(name).unwrap_or(false) {
                    return Err(exceptions::PyTypeError::new_err(
                        "Only wildcards can be restricted.",
                    ));
                }

                Ok(PythonPatternRestriction {
                    restrictions: Arc::new(vec![SimplePatternRestriction::IsLiteralWildcard(name)]),
                })
            }
            _ => Err(exceptions::PyTypeError::new_err(
                "Only wildcards can be restricted.",
            )),
        }
    }

    fn __richcmp__(&self, other: i64, op: CompareOp) -> PyResult<PythonPatternRestriction> {
        match self.expr.to_view() {
            AtomView::Var(v) => {
                let name = v.get_name();
                if !STATE.read().unwrap().is_wildcard(name).unwrap_or(false) {
                    return Err(exceptions::PyTypeError::new_err(
                        "Only wildcards can be restricted.",
                    ));
                }

                Ok(PythonPatternRestriction {
                    restrictions: Arc::new(vec![SimplePatternRestriction::NumberCmp(
                        name, op, other,
                    )]),
                })
            }
            _ => Err(exceptions::PyTypeError::new_err(
                "Only wildcards can be restricted.",
            )),
        }
    }

    fn __iter__(&self) -> PyResult<PythonAtomIterator> {
        match self.expr.to_view() {
            AtomView::Add(_) | AtomView::Mul(_) | AtomView::Fun(_) => {}
            x => {
                return Err(exceptions::PyValueError::new_err(format!(
                    "Non-iterable type: {:?}",
                    x
                )));
            }
        };

        Ok(PythonAtomIterator::from_expr(self.clone()))
    }

    pub fn map(&self, op: PythonPattern) -> PyResult<PythonExpression> {
        let t = match op.expr.as_ref() {
            Pattern::Transformer(t) => t,
            _ => {
                return Err(exceptions::PyValueError::new_err(format!(
                    "Operation must of a transformer",
                )));
            }
        };

        let mut stream = TermStreamer::new_from((*self.expr).clone());

        // map every term in the expression
        stream = stream.map(|workspace, x| {
            let mut out = OwnedAtom::new();
            let restrictions = HashMap::default();
            let mut match_stack = MatchStack::new(&restrictions);
            match_stack.insert(INPUT_ID, Match::Single(x.to_view()));

            t.execute(
                STATE.read().unwrap().borrow(),
                workspace,
                &match_stack,
                &mut out,
            );
            out
        });

        let b = WORKSPACE
            .with(|workspace| stream.to_expression(workspace, STATE.read().unwrap().borrow()));

        Ok(PythonExpression { expr: Arc::new(b) })
    }

    pub fn set_coefficient_ring(&self, vars: Vec<PythonExpression>) -> PyResult<PythonExpression> {
        let mut var_map: SmallVec<[Identifier; INLINED_EXPONENTS]> = SmallVec::new();
        for v in vars {
            match v.expr.to_view() {
                AtomView::Var(v) => var_map.push(v.get_name()),
                e => {
                    Err(exceptions::PyValueError::new_err(format!(
                        "Expected variable instead of {:?}",
                        e
                    )))?;
                }
            }
        }

        let b = WORKSPACE.with(|workspace| {
            let mut b = OwnedAtom::new();
            self.expr.to_view().set_coefficient_ring(
                &var_map,
                STATE.read().unwrap().borrow(),
                workspace,
                &mut b,
            );
            b
        });

        Ok(PythonExpression { expr: Arc::new(b) })
    }

    pub fn expand(&self) -> PythonExpression {
        let b = WORKSPACE.with(|workspace| {
            let mut b = OwnedAtom::new();
            self.expr
                .to_view()
                .expand(workspace, STATE.read().unwrap().borrow(), &mut b);
            b
        });

        PythonExpression { expr: Arc::new(b) }
    }

    pub fn to_polynomial(&self, vars: Option<Vec<PythonExpression>>) -> PyResult<PythonPolynomial> {
        let mut var_map: SmallVec<[Identifier; INLINED_EXPONENTS]> = SmallVec::new();

        if let Some(vm) = vars {
            for v in vm {
                match v.expr.to_view() {
                    AtomView::Var(v) => var_map.push(v.get_name()),
                    e => {
                        Err(exceptions::PyValueError::new_err(format!(
                            "Expected variable instead of {:?}",
                            e
                        )))?;
                    }
                }
            }
        }

        self.expr
            .to_view()
            .to_polynomial(
                RationalField::new(),
                if var_map.is_empty() {
                    None
                } else {
                    Some(var_map.as_slice())
                },
            )
            .map(|x| PythonPolynomial { poly: Arc::new(x) })
            .map_err(|e| {
                exceptions::PyValueError::new_err(format!(
                    "Could not convert to polynomial: {:?}",
                    e
                ))
            })
    }

    pub fn to_rational_polynomial(
        &self,
        vars: Option<Vec<PythonExpression>>,
    ) -> PyResult<PythonRationalPolynomial> {
        let mut var_map: SmallVec<[Identifier; INLINED_EXPONENTS]> = SmallVec::new();

        if let Some(vm) = vars {
            for v in vm {
                match v.expr.to_view() {
                    AtomView::Var(v) => var_map.push(v.get_name()),
                    e => {
                        Err(exceptions::PyValueError::new_err(format!(
                            "Expected variable instead of {:?}",
                            e
                        )))?;
                    }
                }
            }
        }

        WORKSPACE.with(|workspace| {
            self.expr
                .to_view()
                .to_rational_polynomial(
                    workspace,
                    &STATE.read().unwrap(),
                    RationalField::new(),
                    IntegerRing::new(),
                    if var_map.is_empty() {
                        None
                    } else {
                        Some(var_map.as_slice())
                    },
                )
                .map(|x| PythonRationalPolynomial { poly: Arc::new(x) })
                .map_err(|e| {
                    exceptions::PyValueError::new_err(format!(
                        "Could not convert to polynomial: {:?}",
                        e
                    ))
                })
        })
    }

    // TODO: use macro as the body is the same as for to_rational_polynomial
    pub fn to_rational_polynomial_small_exponent(
        &self,
        vars: Option<Vec<PythonExpression>>,
    ) -> PyResult<PythonRationalPolynomialSmallExponent> {
        let mut var_map: SmallVec<[Identifier; INLINED_EXPONENTS]> = SmallVec::new();

        if let Some(vm) = vars {
            for v in vm {
                match v.expr.to_view() {
                    AtomView::Var(v) => var_map.push(v.get_name()),
                    e => {
                        Err(exceptions::PyValueError::new_err(format!(
                            "Expected variable instead of {:?}",
                            e
                        )))?;
                    }
                }
            }
        }

        WORKSPACE.with(|workspace| {
            self.expr
                .to_view()
                .to_rational_polynomial(
                    workspace,
                    &STATE.read().unwrap(),
                    RationalField::new(),
                    IntegerRing::new(),
                    if var_map.is_empty() {
                        None
                    } else {
                        Some(var_map.as_slice())
                    },
                )
                .map(|x| PythonRationalPolynomialSmallExponent { poly: Arc::new(x) })
                .map_err(|e| {
                    exceptions::PyValueError::new_err(format!(
                        "Could not convert to polynomial: {:?}",
                        e
                    ))
                })
        })
    }

    #[pyo3(name = "r#match")]
    pub fn pattern_match(
        &self,
        lhs: ConvertibleToPattern,
        cond: Option<PythonPatternRestriction>,
    ) -> PythonMatchIterator {
        let restrictions = cond.map(|r| r.convert()).unwrap_or(HashMap::default());
        PythonMatchIterator::new(
            (
                lhs.to_pattern().expr,
                self.expr.clone(),
                restrictions,
                STATE.read().unwrap().clone(), // FIXME: state is cloned
            ),
            move |(lhs, target, res, state)| {
                PatternAtomTreeIterator::new(lhs, target.to_view(), state, res)
            },
        )
    }

    pub fn replace_all(
        &self,
        lhs: ConvertibleToPattern,
        rhs: ConvertibleToPattern,
        cond: Option<PythonPatternRestriction>,
    ) -> PyResult<PythonExpression> {
        let pattern = &lhs.to_pattern().expr;
        let rhs = &rhs.to_pattern().expr;
        let restrictions = cond.map(|r| r.convert()).unwrap_or(HashMap::default());
        let mut out = OwnedAtom::new();

        WORKSPACE.with(|workspace| {
            pattern.replace_all(
                self.expr.to_view(),
                &rhs,
                &STATE.read().unwrap(),
                workspace,
                &restrictions,
                &mut out,
            );
        });

        Ok(PythonExpression {
            expr: Arc::new(out),
        })
    }
}

/// A function class for python that constructs an `Expression` when called with arguments.
/// This allows to write:
/// ```python
/// f = Function("f")
/// e = f(1,2,3)
/// ```
#[pyclass(name = "Function")]
pub struct PythonFunction {
    id: Identifier,
}

#[pymethods]
impl PythonFunction {
    #[new]
    pub fn __new__(name: &str) -> PyResult<Self> {
        // TODO: parse and check if this is a valid function name
        let id = STATE.write().unwrap().borrow_mut().get_or_insert_var(name);
        Ok(PythonFunction { id })
    }

    #[getter]
    fn get_w(&mut self) -> PythonFunction {
        PythonFunction { id: self.id }
    }

    #[pyo3(signature = (*args,))]
    pub fn __call__(&self, args: &PyTuple, py: Python) -> PyResult<PyObject> {
        let mut fn_args = Vec::with_capacity(args.len());

        for arg in args {
            if let Ok(a) = arg.extract::<ConvertibleToExpression>() {
                fn_args.push(Pattern::Literal((*a.to_expression().expr).clone()));
            } else if let Ok(a) = arg.extract::<ConvertibleToPattern>() {
                fn_args.push((*a.to_pattern().expr).clone());
            } else {
                let msg = format!("Unknown type: {}", arg.get_type().name().unwrap());
                return Err(exceptions::PyTypeError::new_err(msg));
            }
        }

        if fn_args.iter().all(|x| matches!(x, Pattern::Literal(_))) {
            // simplify to literal expression
            WORKSPACE.with(|workspace| {
                let mut fun_b = workspace.new_atom();
                let fun: &mut OwnedFunD = fun_b.transform_to_fun();
                fun.set_from_name(self.id);
                fun.set_dirty(true);

                for x in fn_args {
                    if let Pattern::Literal(a) = x {
                        fun.add_arg(a.to_view());
                    }
                }

                let mut out = OwnedAtom::new();
                fun_b
                    .get()
                    .to_view()
                    .normalize(workspace, &STATE.read().unwrap(), &mut out);

                Ok(PythonExpression {
                    expr: Arc::new(out),
                }
                .into_py(py))
            })
        } else {
            let p = Pattern::Fn(
                self.id,
                STATE.read().unwrap().is_wildcard(self.id).unwrap(),
                fn_args,
            );
            Ok(PythonPattern { expr: Arc::new(p) }.into_py(py))
        }
    }
}

self_cell!(
    #[pyclass]
    pub struct PythonAtomIterator {
        owner: Arc<OwnedAtom<DefaultRepresentation>>,
        #[covariant]
        dependent: ListIteratorD,
    }
);

impl PythonAtomIterator {
    /// Create a self-referential structure for the iterator.
    pub fn from_expr(expr: PythonExpression) -> PythonAtomIterator {
        PythonAtomIterator::new(expr.expr, |expr| match expr.to_view() {
            AtomView::Add(a) => a.iter(),
            AtomView::Mul(m) => m.iter(),
            AtomView::Fun(f) => f.iter(),
            _ => unreachable!(),
        })
    }
}

#[pymethods]
impl PythonAtomIterator {
    fn __next__(&mut self) -> Option<PythonExpression> {
        self.with_dependent_mut(|_, i| {
            i.next().map(|e| PythonExpression {
                expr: Arc::new({
                    let mut owned = OwnedAtom::new();
                    owned.from_view(&e);
                    owned
                }),
            })
        })
    }
}

type OwnedMatch = (
    Arc<Pattern<DefaultRepresentation>>,
    Arc<OwnedAtom<DefaultRepresentation>>,
    HashMap<Identifier, Vec<PatternRestriction<DefaultRepresentation>>>,
    State,
);
type MatchIterator<'a> = PatternAtomTreeIterator<'a, 'a, DefaultRepresentation>;

self_cell!(
    #[pyclass]
    pub struct PythonMatchIterator {
        owner: OwnedMatch,
        #[not_covariant]
        dependent: MatchIterator,
    }
);

#[pymethods]
impl PythonMatchIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self) -> Option<Vec<(PythonExpression, PythonExpression)>> {
        self.with_dependent_mut(|_, i| {
            i.next().map(|(_, _, _, matches)| {
                matches
                    .into_iter()
                    .map(|m| {
                        (
                            PythonExpression {
                                expr: Arc::new({
                                    let mut a: OwnedAtom<DefaultRepresentation> = OwnedAtom::new();
                                    a.transform_to_var().set_from_id(m.0);
                                    a
                                }),
                            },
                            PythonExpression {
                                expr: Arc::new({
                                    let mut a: OwnedAtom<DefaultRepresentation> = OwnedAtom::new();
                                    m.1.to_atom(&mut a);
                                    a
                                }),
                            },
                        )
                    })
                    .collect()
            })
        })
    }
}

#[pyclass(name = "Polynomial")]
#[derive(Clone)]
pub struct PythonPolynomial {
    pub poly: Arc<MultivariatePolynomial<RationalField, u32>>,
}

#[pymethods]
impl PythonPolynomial {
    pub fn to_integer_polynomial(&self) -> PyResult<PythonIntegerPolynomial> {
        let mut poly_int = MultivariatePolynomial::new(
            self.poly.nvars,
            IntegerRing::new(),
            Some(self.poly.nterms),
            self.poly.var_map.as_ref().map(|x| x.as_slice()),
        );

        let mut new_exponent = SmallVec::<[u8; 5]>::new();

        for t in self.poly.into_iter() {
            if !t.coefficient.is_integer() {
                Err(exceptions::PyValueError::new_err(format!(
                    "Coefficient {} is not an integer",
                    t.coefficient
                )))?;
            }

            new_exponent.clear();
            for e in t.exponents {
                if *e > u8::MAX as u32 {
                    Err(exceptions::PyValueError::new_err(format!(
                        "Exponent {} is too large",
                        e
                    )))?;
                }
                new_exponent.push(*e as u8);
            }

            poly_int.append_monomial(t.coefficient.numerator(), &new_exponent);
        }

        Ok(PythonIntegerPolynomial {
            poly: Arc::new(poly_int),
        })
    }
}

#[pyclass(name = "IntegerPolynomial")]
#[derive(Clone)]
pub struct PythonIntegerPolynomial {
    pub poly: Arc<MultivariatePolynomial<IntegerRing, u8>>,
}

macro_rules! generate_methods {
    ($type:ty) => {
        #[pymethods]
        impl $type {
            pub fn __copy__(&self) -> Self {
                Self {
                    poly: Arc::new((*self.poly).clone()),
                }
            }

            pub fn __str__(&self) -> PyResult<String> {
                Ok(format!(
                    "{}",
                    PolynomialPrinter {
                        poly: &self.poly,
                        state: &STATE.read().unwrap(),
                        print_mode: PrintMode::default()
                    }
                ))
            }

            pub fn __repr__(&self) -> PyResult<String> {
                Ok(format!("{:?}", self.poly))
            }

            pub fn __add__(&self, rhs: Self) -> Self {
                if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    Self {
                        poly: Arc::new((*self.poly).clone() + (*rhs.poly).clone()),
                    }
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);
                    Self {
                        poly: Arc::new(new_self + new_rhs),
                    }
                }
            }

            pub fn __sub__(&self, rhs: Self) -> Self {
                self.__add__(rhs.__neg__())
            }

            pub fn __mul__(&self, rhs: Self) -> Self {
                if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    Self {
                        poly: Arc::new(&*self.poly * &*rhs.poly),
                    }
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);
                    Self {
                        poly: Arc::new(new_self * &new_rhs),
                    }
                }
            }

            pub fn __truediv__(&self, rhs: Self) -> PyResult<Self> {
                let (q, r) = if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    self.poly.quot_rem(&rhs.poly, false)
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);

                    new_self.quot_rem(&new_rhs, false)
                };

                if r.is_zero() {
                    Ok(Self { poly: Arc::new(q) })
                } else {
                    Err(exceptions::PyValueError::new_err(format!(
                        "The division has a remainder: {}",
                        r
                    )))
                }
            }

            pub fn quot_rem(&self, rhs: Self) -> (Self, Self) {
                if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    let (q, r) = self.poly.quot_rem(&rhs.poly, false);

                    (Self { poly: Arc::new(q) }, Self { poly: Arc::new(r) })
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);

                    let (q, r) = new_self.quot_rem(&new_rhs, false);

                    (Self { poly: Arc::new(q) }, Self { poly: Arc::new(r) })
                }
            }

            pub fn __neg__(&self) -> Self {
                Self {
                    poly: Arc::new((*self.poly).clone().neg()),
                }
            }

            pub fn gcd(&self, rhs: Self) -> Self {
                if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    Self {
                        poly: Arc::new(MultivariatePolynomial::gcd(&self.poly, &rhs.poly)),
                    }
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);
                    Self {
                        poly: Arc::new(MultivariatePolynomial::gcd(&new_self, &new_rhs)),
                    }
                }
            }
        }
    };
}

generate_methods!(PythonPolynomial);
generate_methods!(PythonIntegerPolynomial);

#[pyclass(name = "RationalPolynomial")]
#[derive(Clone)]
pub struct PythonRationalPolynomial {
    pub poly: Arc<RationalPolynomial<IntegerRing, u32>>,
}

#[pymethods]
impl PythonRationalPolynomial {
    #[new]
    pub fn __new__(num: &PythonPolynomial, den: &PythonPolynomial) -> Self {
        Self {
            poly: Arc::new(RationalPolynomial::from_num_den(
                (*num.poly).clone(),
                (*den.poly).clone(),
                IntegerRing::new(),
                true,
            )),
        }
    }
}

#[pyclass(name = "RationalPolynomialSmallExponent")]
#[derive(Clone)]
pub struct PythonRationalPolynomialSmallExponent {
    pub poly: Arc<RationalPolynomial<IntegerRing, u8>>,
}

// TODO: unify with polynomial methods
macro_rules! generate_rat_methods {
    ($type:ty) => {
        #[pymethods]
        impl $type {
            pub fn __copy__(&self) -> Self {
                Self {
                    poly: Arc::new((*self.poly).clone()),
                }
            }

            pub fn __str__(&self) -> PyResult<String> {
                Ok(format!(
                    "{}",
                    RationalPolynomialPrinter {
                        poly: &self.poly,
                        state: &STATE.read().unwrap(),
                        print_mode: PrintMode::default()
                    }
                ))
            }

            pub fn __repr__(&self) -> PyResult<String> {
                Ok(format!("{:?}", self.poly))
            }

            pub fn __add__(&self, rhs: Self) -> Self {
                if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    Self {
                        poly: Arc::new(&*self.poly + &*rhs.poly),
                    }
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);
                    Self {
                        poly: Arc::new(&new_self + &new_rhs),
                    }
                }
            }

            pub fn __sub__(&self, rhs: Self) -> Self {
                if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    Self {
                        poly: Arc::new(&*self.poly - &*rhs.poly),
                    }
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);
                    Self {
                        poly: Arc::new(&new_self - &new_rhs),
                    }
                }
            }

            pub fn __mul__(&self, rhs: Self) -> Self {
                if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    Self {
                        poly: Arc::new(&*self.poly * &*rhs.poly),
                    }
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);
                    Self {
                        poly: Arc::new(&new_self * &new_rhs),
                    }
                }
            }

            pub fn __truediv__(&self, rhs: Self) -> Self {
                if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    Self {
                        poly: Arc::new(&*self.poly * &*rhs.poly),
                    }
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);
                    Self {
                        poly: Arc::new(&new_self / &new_rhs),
                    }
                }
            }

            pub fn __neg__(&self) -> Self {
                Self {
                    poly: Arc::new((*self.poly).clone().neg()),
                }
            }

            pub fn gcd(&self, rhs: Self) -> Self {
                if self.poly.get_var_map() == rhs.poly.get_var_map() {
                    Self {
                        poly: Arc::new(self.poly.gcd(&rhs.poly)),
                    }
                } else {
                    let mut new_self = (*self.poly).clone();
                    let mut new_rhs = (*rhs.poly).clone();
                    new_self.unify_var_map(&mut new_rhs);
                    Self {
                        poly: Arc::new(new_self.gcd(&new_rhs)),
                    }
                }
            }
        }
    };
}

generate_rat_methods!(PythonRationalPolynomial);
generate_rat_methods!(PythonRationalPolynomialSmallExponent);
