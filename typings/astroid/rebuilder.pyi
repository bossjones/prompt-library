"""
This type stub file was generated by pyright.
"""

import ast
import sys
from typing import Final, TYPE_CHECKING, TypeVar, Union, overload
from astroid import nodes
from astroid._ast import ParserModule
from astroid.manager import AstroidManager
from astroid.nodes import NodeNG
from astroid.nodes.node_classes import AssignName

"""This module contains utilities for rebuilding an _ast tree in
order to get a single Astroid representation.
"""
REDIRECT: Final[dict[str, str]] = ...
T_Doc = TypeVar("T_Doc", "ast.Module", "ast.ClassDef", Union["ast.FunctionDef", "ast.AsyncFunctionDef"])
_FunctionT = TypeVar("_FunctionT", nodes.FunctionDef, nodes.AsyncFunctionDef)
_ForT = TypeVar("_ForT", nodes.For, nodes.AsyncFor)
_WithT = TypeVar("_WithT", nodes.With, nodes.AsyncWith)
NodesWithDocsType = Union[nodes.Module, nodes.ClassDef, nodes.FunctionDef]
class TreeRebuilder:
    """Rebuilds the _ast tree to become an Astroid tree."""
    def __init__(self, manager: AstroidManager, parser_module: ParserModule | None = ..., data: str | None = ...) -> None:
        ...

    def visit_module(self, node: ast.Module, modname: str, modpath: str, package: bool) -> nodes.Module:
        """Visit a Module node by returning a fresh instance of it.

        Note: Method not called by 'visit'
        """
        ...

    if TYPE_CHECKING:
        @overload
        def visit(self, node: ast.arg, parent: NodeNG) -> nodes.AssignName:
            ...

        @overload
        def visit(self, node: ast.arguments, parent: NodeNG) -> nodes.Arguments:
            ...

        @overload
        def visit(self, node: ast.Assert, parent: NodeNG) -> nodes.Assert:
            ...

        @overload
        def visit(self, node: ast.AsyncFunctionDef, parent: NodeNG) -> nodes.AsyncFunctionDef:
            ...

        @overload
        def visit(self, node: ast.AsyncFor, parent: NodeNG) -> nodes.AsyncFor:
            ...

        @overload
        def visit(self, node: ast.Await, parent: NodeNG) -> nodes.Await:
            ...

        @overload
        def visit(self, node: ast.AsyncWith, parent: NodeNG) -> nodes.AsyncWith:
            ...

        @overload
        def visit(self, node: ast.Assign, parent: NodeNG) -> nodes.Assign:
            ...

        @overload
        def visit(self, node: ast.AnnAssign, parent: NodeNG) -> nodes.AnnAssign:
            ...

        @overload
        def visit(self, node: ast.AugAssign, parent: NodeNG) -> nodes.AugAssign:
            ...

        @overload
        def visit(self, node: ast.BinOp, parent: NodeNG) -> nodes.BinOp:
            ...

        @overload
        def visit(self, node: ast.BoolOp, parent: NodeNG) -> nodes.BoolOp:
            ...

        @overload
        def visit(self, node: ast.Break, parent: NodeNG) -> nodes.Break:
            ...

        @overload
        def visit(self, node: ast.Call, parent: NodeNG) -> nodes.Call:
            ...

        @overload
        def visit(self, node: ast.ClassDef, parent: NodeNG) -> nodes.ClassDef:
            ...

        @overload
        def visit(self, node: ast.Continue, parent: NodeNG) -> nodes.Continue:
            ...

        @overload
        def visit(self, node: ast.Compare, parent: NodeNG) -> nodes.Compare:
            ...

        @overload
        def visit(self, node: ast.comprehension, parent: NodeNG) -> nodes.Comprehension:
            ...

        @overload
        def visit(self, node: ast.Delete, parent: NodeNG) -> nodes.Delete:
            ...

        @overload
        def visit(self, node: ast.Dict, parent: NodeNG) -> nodes.Dict:
            ...

        @overload
        def visit(self, node: ast.DictComp, parent: NodeNG) -> nodes.DictComp:
            ...

        @overload
        def visit(self, node: ast.Expr, parent: NodeNG) -> nodes.Expr:
            ...

        @overload
        def visit(self, node: ast.ExceptHandler, parent: NodeNG) -> nodes.ExceptHandler:
            ...

        @overload
        def visit(self, node: ast.For, parent: NodeNG) -> nodes.For:
            ...

        @overload
        def visit(self, node: ast.ImportFrom, parent: NodeNG) -> nodes.ImportFrom:
            ...

        @overload
        def visit(self, node: ast.FunctionDef, parent: NodeNG) -> nodes.FunctionDef:
            ...

        @overload
        def visit(self, node: ast.GeneratorExp, parent: NodeNG) -> nodes.GeneratorExp:
            ...

        @overload
        def visit(self, node: ast.Attribute, parent: NodeNG) -> nodes.Attribute:
            ...

        @overload
        def visit(self, node: ast.Global, parent: NodeNG) -> nodes.Global:
            ...

        @overload
        def visit(self, node: ast.If, parent: NodeNG) -> nodes.If:
            ...

        @overload
        def visit(self, node: ast.IfExp, parent: NodeNG) -> nodes.IfExp:
            ...

        @overload
        def visit(self, node: ast.Import, parent: NodeNG) -> nodes.Import:
            ...

        @overload
        def visit(self, node: ast.JoinedStr, parent: NodeNG) -> nodes.JoinedStr:
            ...

        @overload
        def visit(self, node: ast.FormattedValue, parent: NodeNG) -> nodes.FormattedValue:
            ...

        @overload
        def visit(self, node: ast.NamedExpr, parent: NodeNG) -> nodes.NamedExpr:
            ...

        @overload
        def visit(self, node: ast.keyword, parent: NodeNG) -> nodes.Keyword:
            ...

        @overload
        def visit(self, node: ast.Lambda, parent: NodeNG) -> nodes.Lambda:
            ...

        @overload
        def visit(self, node: ast.List, parent: NodeNG) -> nodes.List:
            ...

        @overload
        def visit(self, node: ast.ListComp, parent: NodeNG) -> nodes.ListComp:
            ...

        @overload
        def visit(self, node: ast.Name, parent: NodeNG) -> nodes.Name | nodes.Const | nodes.AssignName | nodes.DelName:
            ...

        @overload
        def visit(self, node: ast.Nonlocal, parent: NodeNG) -> nodes.Nonlocal:
            ...

        @overload
        def visit(self, node: ast.Constant, parent: NodeNG) -> nodes.Const:
            ...

        @overload
        def visit(self, node: ast.Pass, parent: NodeNG) -> nodes.Pass:
            ...

        @overload
        def visit(self, node: ast.Raise, parent: NodeNG) -> nodes.Raise:
            ...

        @overload
        def visit(self, node: ast.Return, parent: NodeNG) -> nodes.Return:
            ...

        @overload
        def visit(self, node: ast.Set, parent: NodeNG) -> nodes.Set:
            ...

        @overload
        def visit(self, node: ast.SetComp, parent: NodeNG) -> nodes.SetComp:
            ...

        @overload
        def visit(self, node: ast.Slice, parent: nodes.Subscript) -> nodes.Slice:
            ...

        @overload
        def visit(self, node: ast.Subscript, parent: NodeNG) -> nodes.Subscript:
            ...

        @overload
        def visit(self, node: ast.Starred, parent: NodeNG) -> nodes.Starred:
            ...

        @overload
        def visit(self, node: ast.Try, parent: NodeNG) -> nodes.Try:
            ...

        @overload
        def visit(self, node: ast.Tuple, parent: NodeNG) -> nodes.Tuple:
            ...

        @overload
        def visit(self, node: ast.UnaryOp, parent: NodeNG) -> nodes.UnaryOp:
            ...

        @overload
        def visit(self, node: ast.While, parent: NodeNG) -> nodes.While:
            ...

        @overload
        def visit(self, node: ast.With, parent: NodeNG) -> nodes.With:
            ...

        @overload
        def visit(self, node: ast.Yield, parent: NodeNG) -> nodes.Yield:
            ...

        @overload
        def visit(self, node: ast.YieldFrom, parent: NodeNG) -> nodes.YieldFrom:
            ...

        @overload
        def visit(self, node: ast.AST, parent: NodeNG) -> NodeNG:
            ...

        @overload
        def visit(self, node: None, parent: NodeNG) -> None:
            ...

    def visit(self, node: ast.AST | None, parent: NodeNG) -> NodeNG | None:
        ...

    def visit_arg(self, node: ast.arg, parent: NodeNG) -> nodes.AssignName:
        """Visit an arg node by returning a fresh AssName instance."""
        ...

    def visit_arguments(self, node: ast.arguments, parent: NodeNG) -> nodes.Arguments:
        """Visit an Arguments node by returning a fresh instance of it."""
        ...

    def visit_assert(self, node: ast.Assert, parent: NodeNG) -> nodes.Assert:
        """Visit a Assert node by returning a fresh instance of it."""
        ...

    def check_type_comment(self, node: ast.Assign | ast.arg | ast.For | ast.AsyncFor | ast.With | ast.AsyncWith, parent: (nodes.Assign | nodes.Arguments | nodes.For | nodes.AsyncFor | nodes.With | nodes.AsyncWith)) -> NodeNG | None:
        ...

    def check_function_type_comment(self, node: ast.FunctionDef | ast.AsyncFunctionDef, parent: NodeNG) -> tuple[NodeNG | None, list[NodeNG]] | None:
        ...

    def visit_asyncfunctiondef(self, node: ast.AsyncFunctionDef, parent: NodeNG) -> nodes.AsyncFunctionDef:
        ...

    def visit_asyncfor(self, node: ast.AsyncFor, parent: NodeNG) -> nodes.AsyncFor:
        ...

    def visit_await(self, node: ast.Await, parent: NodeNG) -> nodes.Await:
        ...

    def visit_asyncwith(self, node: ast.AsyncWith, parent: NodeNG) -> nodes.AsyncWith:
        ...

    def visit_assign(self, node: ast.Assign, parent: NodeNG) -> nodes.Assign:
        """Visit a Assign node by returning a fresh instance of it."""
        ...

    def visit_annassign(self, node: ast.AnnAssign, parent: NodeNG) -> nodes.AnnAssign:
        """Visit an AnnAssign node by returning a fresh instance of it."""
        ...

    @overload
    def visit_assignname(self, node: ast.AST, parent: NodeNG, node_name: str) -> nodes.AssignName:
        ...

    @overload
    def visit_assignname(self, node: ast.AST, parent: NodeNG, node_name: None) -> None:
        ...

    def visit_assignname(self, node: ast.AST, parent: NodeNG, node_name: str | None) -> nodes.AssignName | None:
        """Visit a node and return a AssignName node.

        Note: Method not called by 'visit'
        """
        ...

    def visit_augassign(self, node: ast.AugAssign, parent: NodeNG) -> nodes.AugAssign:
        """Visit a AugAssign node by returning a fresh instance of it."""
        ...

    def visit_binop(self, node: ast.BinOp, parent: NodeNG) -> nodes.BinOp:
        """Visit a BinOp node by returning a fresh instance of it."""
        ...

    def visit_boolop(self, node: ast.BoolOp, parent: NodeNG) -> nodes.BoolOp:
        """Visit a BoolOp node by returning a fresh instance of it."""
        ...

    def visit_break(self, node: ast.Break, parent: NodeNG) -> nodes.Break:
        """Visit a Break node by returning a fresh instance of it."""
        ...

    def visit_call(self, node: ast.Call, parent: NodeNG) -> nodes.Call:
        """Visit a CallFunc node by returning a fresh instance of it."""
        ...

    def visit_classdef(self, node: ast.ClassDef, parent: NodeNG, newstyle: bool = ...) -> nodes.ClassDef:
        """Visit a ClassDef node to become astroid."""
        ...

    def visit_continue(self, node: ast.Continue, parent: NodeNG) -> nodes.Continue:
        """Visit a Continue node by returning a fresh instance of it."""
        ...

    def visit_compare(self, node: ast.Compare, parent: NodeNG) -> nodes.Compare:
        """Visit a Compare node by returning a fresh instance of it."""
        ...

    def visit_comprehension(self, node: ast.comprehension, parent: NodeNG) -> nodes.Comprehension:
        """Visit a Comprehension node by returning a fresh instance of it."""
        ...

    def visit_decorators(self, node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef, parent: NodeNG) -> nodes.Decorators | None:
        """Visit a Decorators node by returning a fresh instance of it.

        Note: Method not called by 'visit'
        """
        ...

    def visit_delete(self, node: ast.Delete, parent: NodeNG) -> nodes.Delete:
        """Visit a Delete node by returning a fresh instance of it."""
        ...

    def visit_dict(self, node: ast.Dict, parent: NodeNG) -> nodes.Dict:
        """Visit a Dict node by returning a fresh instance of it."""
        ...

    def visit_dictcomp(self, node: ast.DictComp, parent: NodeNG) -> nodes.DictComp:
        """Visit a DictComp node by returning a fresh instance of it."""
        ...

    def visit_expr(self, node: ast.Expr, parent: NodeNG) -> nodes.Expr:
        """Visit a Expr node by returning a fresh instance of it."""
        ...

    def visit_excepthandler(self, node: ast.ExceptHandler, parent: NodeNG) -> nodes.ExceptHandler:
        """Visit an ExceptHandler node by returning a fresh instance of it."""
        ...

    def visit_for(self, node: ast.For, parent: NodeNG) -> nodes.For:
        ...

    def visit_importfrom(self, node: ast.ImportFrom, parent: NodeNG) -> nodes.ImportFrom:
        """Visit an ImportFrom node by returning a fresh instance of it."""
        ...

    def visit_functiondef(self, node: ast.FunctionDef, parent: NodeNG) -> nodes.FunctionDef:
        ...

    def visit_generatorexp(self, node: ast.GeneratorExp, parent: NodeNG) -> nodes.GeneratorExp:
        """Visit a GeneratorExp node by returning a fresh instance of it."""
        ...

    def visit_attribute(self, node: ast.Attribute, parent: NodeNG) -> nodes.Attribute | nodes.AssignAttr | nodes.DelAttr:
        """Visit an Attribute node by returning a fresh instance of it."""
        ...

    def visit_global(self, node: ast.Global, parent: NodeNG) -> nodes.Global:
        """Visit a Global node to become astroid."""
        ...

    def visit_if(self, node: ast.If, parent: NodeNG) -> nodes.If:
        """Visit an If node by returning a fresh instance of it."""
        ...

    def visit_ifexp(self, node: ast.IfExp, parent: NodeNG) -> nodes.IfExp:
        """Visit a IfExp node by returning a fresh instance of it."""
        ...

    def visit_import(self, node: ast.Import, parent: NodeNG) -> nodes.Import:
        """Visit a Import node by returning a fresh instance of it."""
        ...

    def visit_joinedstr(self, node: ast.JoinedStr, parent: NodeNG) -> nodes.JoinedStr:
        ...

    def visit_formattedvalue(self, node: ast.FormattedValue, parent: NodeNG) -> nodes.FormattedValue:
        ...

    def visit_namedexpr(self, node: ast.NamedExpr, parent: NodeNG) -> nodes.NamedExpr:
        ...

    def visit_keyword(self, node: ast.keyword, parent: NodeNG) -> nodes.Keyword:
        """Visit a Keyword node by returning a fresh instance of it."""
        ...

    def visit_lambda(self, node: ast.Lambda, parent: NodeNG) -> nodes.Lambda:
        """Visit a Lambda node by returning a fresh instance of it."""
        ...

    def visit_list(self, node: ast.List, parent: NodeNG) -> nodes.List:
        """Visit a List node by returning a fresh instance of it."""
        ...

    def visit_listcomp(self, node: ast.ListComp, parent: NodeNG) -> nodes.ListComp:
        """Visit a ListComp node by returning a fresh instance of it."""
        ...

    def visit_name(self, node: ast.Name, parent: NodeNG) -> nodes.Name | nodes.AssignName | nodes.DelName:
        """Visit a Name node by returning a fresh instance of it."""
        ...

    def visit_nonlocal(self, node: ast.Nonlocal, parent: NodeNG) -> nodes.Nonlocal:
        """Visit a Nonlocal node and return a new instance of it."""
        ...

    def visit_constant(self, node: ast.Constant, parent: NodeNG) -> nodes.Const:
        """Visit a Constant node by returning a fresh instance of Const."""
        ...

    def visit_paramspec(self, node: ast.ParamSpec, parent: NodeNG) -> nodes.ParamSpec:
        """Visit a ParamSpec node by returning a fresh instance of it."""
        ...

    def visit_pass(self, node: ast.Pass, parent: NodeNG) -> nodes.Pass:
        """Visit a Pass node by returning a fresh instance of it."""
        ...

    def visit_raise(self, node: ast.Raise, parent: NodeNG) -> nodes.Raise:
        """Visit a Raise node by returning a fresh instance of it."""
        ...

    def visit_return(self, node: ast.Return, parent: NodeNG) -> nodes.Return:
        """Visit a Return node by returning a fresh instance of it."""
        ...

    def visit_set(self, node: ast.Set, parent: NodeNG) -> nodes.Set:
        """Visit a Set node by returning a fresh instance of it."""
        ...

    def visit_setcomp(self, node: ast.SetComp, parent: NodeNG) -> nodes.SetComp:
        """Visit a SetComp node by returning a fresh instance of it."""
        ...

    def visit_slice(self, node: ast.Slice, parent: nodes.Subscript) -> nodes.Slice:
        """Visit a Slice node by returning a fresh instance of it."""
        ...

    def visit_subscript(self, node: ast.Subscript, parent: NodeNG) -> nodes.Subscript:
        """Visit a Subscript node by returning a fresh instance of it."""
        ...

    def visit_starred(self, node: ast.Starred, parent: NodeNG) -> nodes.Starred:
        """Visit a Starred node and return a new instance of it."""
        ...

    def visit_try(self, node: ast.Try, parent: NodeNG) -> nodes.Try:
        """Visit a Try node by returning a fresh instance of it"""
        ...

    def visit_trystar(self, node: ast.TryStar, parent: NodeNG) -> nodes.TryStar:
        ...

    def visit_tuple(self, node: ast.Tuple, parent: NodeNG) -> nodes.Tuple:
        """Visit a Tuple node by returning a fresh instance of it."""
        ...

    def visit_typealias(self, node: ast.TypeAlias, parent: NodeNG) -> nodes.TypeAlias:
        """Visit a TypeAlias node by returning a fresh instance of it."""
        ...

    def visit_typevar(self, node: ast.TypeVar, parent: NodeNG) -> nodes.TypeVar:
        """Visit a TypeVar node by returning a fresh instance of it."""
        ...

    def visit_typevartuple(self, node: ast.TypeVarTuple, parent: NodeNG) -> nodes.TypeVarTuple:
        """Visit a TypeVarTuple node by returning a fresh instance of it."""
        ...

    def visit_unaryop(self, node: ast.UnaryOp, parent: NodeNG) -> nodes.UnaryOp:
        """Visit a UnaryOp node by returning a fresh instance of it."""
        ...

    def visit_while(self, node: ast.While, parent: NodeNG) -> nodes.While:
        """Visit a While node by returning a fresh instance of it."""
        ...

    def visit_with(self, node: ast.With, parent: NodeNG) -> NodeNG:
        ...

    def visit_yield(self, node: ast.Yield, parent: NodeNG) -> NodeNG:
        """Visit a Yield node by returning a fresh instance of it."""
        ...

    def visit_yieldfrom(self, node: ast.YieldFrom, parent: NodeNG) -> NodeNG:
        ...

    if sys.version_info >= (3, 10):
        def visit_match(self, node: ast.Match, parent: NodeNG) -> nodes.Match:
            ...

        def visit_matchcase(self, node: ast.match_case, parent: NodeNG) -> nodes.MatchCase:
            ...

        def visit_matchvalue(self, node: ast.MatchValue, parent: NodeNG) -> nodes.MatchValue:
            ...

        def visit_matchsingleton(self, node: ast.MatchSingleton, parent: NodeNG) -> nodes.MatchSingleton:
            ...

        def visit_matchsequence(self, node: ast.MatchSequence, parent: NodeNG) -> nodes.MatchSequence:
            ...

        def visit_matchmapping(self, node: ast.MatchMapping, parent: NodeNG) -> nodes.MatchMapping:
            ...

        def visit_matchclass(self, node: ast.MatchClass, parent: NodeNG) -> nodes.MatchClass:
            ...

        def visit_matchstar(self, node: ast.MatchStar, parent: NodeNG) -> nodes.MatchStar:
            ...

        def visit_matchas(self, node: ast.MatchAs, parent: NodeNG) -> nodes.MatchAs:
            ...

        def visit_matchor(self, node: ast.MatchOr, parent: NodeNG) -> nodes.MatchOr:
            ...
