

TestStringComponent = createScinodeComponent({"name": "TestString", "catalog": "Test", "controls": [["Int", "t"], ["String", "value"]], "inputs": [], "outputs": [["String", "string"]]});
TestFloatComponent = createScinodeComponent({"name": "TestFloat", "catalog": "Test", "controls": [["Int", "t"], ["Float", "value"]], "inputs": [], "outputs": [["Float", "float"]]});
TestAddComponent = createScinodeComponent({"name": "TestAdd", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Float", "result"]]});
TestMinusComponent = createScinodeComponent({"name": "TestMinus", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Float", "result"]]});
TestSqrtComponent = createScinodeComponent({"name": "TestSqrt", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"]], "outputs": [["Float", "result"]]});
TestGreaterComponent = createScinodeComponent({"name": "TestGreater", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Bool", "result"]]});
TestLessComponent = createScinodeComponent({"name": "TestLess", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Bool", "result"]]});
TestRangeComponent = createScinodeComponent({"name": "TestRange", "catalog": "Test", "controls": [["Float", "start"], ["Float", "stop"], ["Float", "step"]], "inputs": [], "outputs": [["Float", "result"]]});
TestEnumComponent = createScinodeComponent({"name": "TestEnum", "catalog": "Test", "controls": [["Int", "t"], ["Enum", "function", {"options": ["add", "sqrt"], "defaultVal": "add"}]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Float", "result"]]});


async function control_callback(node) {
    node.inputs.forEach(function(input, key) {
        // delete data from input control
        delete node.data[input.name];
        // remote the connection
        for (let i = 0; i < input.connections.length; i++) {
            input.connections[i].remove();
        }
        node.removeInput(input);
    })
    node.outputs.forEach(function(output, key) {
        // remote the connection
        for (let i = 0; i < output.connections.length; i++) {
            output.connections[i].remove();
        }
        node.removeOutput(output);
    })
    await node.update();
    node.createSockets(node);
    await node.update();
    setTimeout( () => { this.emitter.view.updateConnections({node}); }, 10);
};


class TestEnumUpdateComponent extends ScinodeComponent {
    constructor(){
        super("TestEnumUpdate");
        this.catalog = 'Test';
        this.name = 'TestEnumUpdate'
    }

    createControls(node, callback) {
        node.addControl(new IntControl(this.editor, 't'));
        var ctl1 = new EnumUpdateControl(this.editor, 'function',
                    {"options": ['add', 'sqrt'], "defaultVal": "add"},
                    callback, node);
        node.addControl(ctl1);
    }

    createSockets(node){
        if (node.data['function'] == undefined || node.data['function'] == 'add') {
            var inp1 = new Rete.Input('x', "x", SocketFloat);
            var inp2 = new Rete.Input('y', "y", SocketFloat);
            var out = new Rete.Output('result', "result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            inp2.addControl(new FloatControl(editor, 'y'))
            node.addInput(inp1)
                .addInput(inp2)
                .addOutput(out);
        }
        else {
            var inp1 = new Rete.Input('x', "x", SocketFloat);
            var out = new Rete.Output('result', "result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            node.addInput(inp1)
                .addOutput(out);
        }
    }

    builder(node) {
        this.init(node);
        node.createSockets = this.createSockets;
        console.log("data: t", node.data['t'])
        this.createControls(node, control_callback);
        this.createSockets(node);
        return node
    }
}


// Numpy
var numpy_function_items = ["DataSource", "MachAr", "Tester", "abs", "absolute", "add", "add_docstring", "add_newdoc", "add_newdoc_ufunc", "alen", "all", "allclose", "alltrue", "amax", "amin", "angle", "any", "append", "apply_along_axis", "apply_over_axes", "arange", "arccos", "arccosh", "arcsin", "arcsinh", "arctan", "arctan2", "arctanh", "argmax", "argmin", "argpartition", "argsort", "argwhere", "around", "array", "array2string", "array_equal", "array_equiv", "array_repr", "array_split", "array_str", "asanyarray", "asarray", "asarray_chkfinite", "ascontiguousarray", "asfarray", "asfortranarray", "asmatrix", "asscalar", "atleast_1d", "atleast_2d", "atleast_3d", "average", "bartlett", "base_repr", "binary_repr", "bincount", "bitwise_and", "bitwise_not", "bitwise_or", "bitwise_xor", "blackman", "block", "bmat", "bool", "bool8", "bool_", "broadcast", "broadcast_arrays", "broadcast_to", "busday_count", "busday_offset", "busdaycalendar", "byte", "byte_bounds", "bytes0", "bytes_", "can_cast", "cbrt", "cdouble", "ceil", "cfloat", "character", "chararray", "choose", "clip", "clongdouble", "clongfloat", "column_stack", "common_type", "compare_chararrays", "complex", "complex128", "complex256", "complex64", "complex_", "complexfloating", "compress", "concatenate", "conj", "conjugate", "convolve", "copy", "copysign", "copyto", "corrcoef", "correlate", "cos", "cosh", "count_nonzero", "cov", "cross", "csingle", "cumprod", "cumproduct", "cumsum", "datetime64", "datetime_as_string", "datetime_data", "deg2rad", "degrees", "delete", "deprecate", "deprecate_with_doc", "diag", "diag_indices", "diag_indices_from", "diagflat", "diagonal", "diff", "digitize", "disp", "divide", "divmod", "dot", "double", "dsplit", "dstack", "dtype", "ediff1d", "einsum", "einsum_path", "empty", "empty_like", "equal", "errstate", "exp", "exp2", "expand_dims", "expm1", "extract", "eye", "fabs", "fastCopyAndTranspose", "fill_diagonal", "find_common_type", "finfo", "fix", "flatiter", "flatnonzero", "flexible", "flip", "fliplr", "flipud", "float", "float128", "float16", "float32", "float64", "float_", "float_power", "floating", "floor", "floor_divide", "fmax", "fmin", "fmod", "format_float_positional", "format_float_scientific", "format_parser", "frexp", "frombuffer", "fromfile", "fromfunction", "fromiter", "frompyfunc", "fromregex", "fromstring", "full", "full_like", "fv", "gcd", "generic", "genfromtxt", "geomspace", "get_array_wrap", "get_include", "get_printoptions", "getbufsize", "geterr", "geterrcall", "geterrobj", "gradient", "greater", "greater_equal", "half", "hamming", "hanning", "heaviside", "histogram", "histogram2d", "histogram_bin_edges", "histogramdd", "hsplit", "hstack", "hypot", "i0", "identity", "iinfo", "imag", "in1d", "indices", "inexact", "info", "inner", "insert", "int", "int0", "int16", "int32", "int64", "int8", "int_", "intc", "integer", "interp", "intersect1d", "intp", "invert", "ipmt", "irr", "is_busday", "isclose", "iscomplex", "iscomplexobj", "isfinite", "isfortran", "isin", "isinf", "isnan", "isnat", "isneginf", "isposinf", "isreal", "isrealobj", "isscalar", "issctype", "issubclass_", "issubdtype", "issubsctype", "iterable", "ix_", "kaiser", "kron", "lcm", "ldexp", "left_shift", "less", "less_equal", "lexsort", "linspace", "load", "loads", "loadtxt", "log", "log10", "log1p", "log2", "logaddexp", "logaddexp2", "logical_and", "logical_not", "logical_or", "logical_xor", "logspace", "long", "longcomplex", "longdouble", "longfloat", "longlong", "lookfor", "mafromtxt", "mask_indices", "mat", "matmul", "matrix", "max", "maximum", "maximum_sctype", "may_share_memory", "mean", "median", "memmap", "meshgrid", "min", "min_scalar_type", "minimum", "mintypecode", "mirr", "mod", "modf", "moveaxis", "msort", "multiply", "nan_to_num", "nanargmax", "nanargmin", "nancumprod", "nancumsum", "nanmax", "nanmean", "nanmedian", "nanmin", "nanpercentile", "nanprod", "nanquantile", "nanstd", "nansum", "nanvar", "ndarray", "ndenumerate", "ndfromtxt", "ndim", "ndindex", "nditer", "negative", "nested_iters", "nextafter", "nonzero", "not_equal", "nper", "npv", "number", "obj2sctype", "object", "object0", "object_", "ones", "ones_like", "outer", "packbits", "pad", "partition", "percentile", "piecewise", "place", "pmt", "poly", "poly1d", "polyadd", "polyder", "polydiv", "polyfit", "polyint", "polymul", "polysub", "polyval", "positive", "power", "ppmt", "printoptions", "prod", "product", "promote_types", "ptp", "put", "put_along_axis", "putmask", "pv", "quantile", "rad2deg", "radians", "rate", "ravel", "ravel_multi_index", "real", "real_if_close", "recarray", "recfromcsv", "recfromtxt", "reciprocal", "record", "remainder", "repeat", "require", "reshape", "resize", "result_type", "right_shift", "rint", "roll", "rollaxis", "roots", "rot90", "round", "round_", "row_stack", "safe_eval", "save", "savetxt", "savez", "savez_compressed", "sctype2char", "searchsorted", "select", "set_numeric_ops", "set_printoptions", "set_string_function", "setbufsize", "setdiff1d", "seterr", "seterrcall", "seterrobj", "setxor1d", "shape", "shares_memory", "short", "show_config", "sign", "signbit", "signedinteger", "sin", "sinc", "single", "singlecomplex", "sinh", "size", "sometrue", "sort", "sort_complex", "source", "spacing", "split", "sqrt", "square", "squeeze", "stack", "std", "str", "str0", "str_", "string_", "subtract", "sum", "swapaxes", "take", "take_along_axis", "tan", "tanh", "tensordot", "test", "tile", "timedelta64", "trace", "transpose", "trapz", "tri", "tril", "tril_indices", "tril_indices_from", "trim_zeros", "triu", "triu_indices", "triu_indices_from", "true_divide", "trunc", "typename", "ubyte", "ufunc", "uint", "uint0", "uint16", "uint32", "uint64", "uint8", "uintc", "uintp", "ulonglong", "unicode", "unicode_", "union1d", "unique", "unpackbits", "unravel_index", "unsignedinteger", "unwrap", "ushort", "vander", "var", "vdot", "vectorize", "void", "void0", "vsplit", "vstack", "where", "who", "zeros", "zeros_like"];
class NumpyComponent extends ScinodeComponent {
    constructor(){
        super("Numpy");
        this.catalog = 'Math';
        this.name = 'Numpy'
    }

    createControls(node, callback) {
        var ctl1 = new EnumUpdateControl(this.editor, 'function',
                    {"options": numpy_function_items, "defaultVal": "add"},
                    callback, node);
        node.addControl(ctl1);
    }

    createSockets(node){
        if (node.data['function'] == undefined || [
            "multiply",
            "divide",
            "power",
            "substract",
            "mod",
            "greater",
            "less",
            "add",
        ].includes(node.data['function'])) {
            var inp1 = new Rete.Input('x1', "x1", SocketFloat);
            var inp2 = new Rete.Input('x2', "x2", SocketFloat);
            var out = new Rete.Output('result', "result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x1'))
            inp2.addControl(new FloatControl(editor, 'x2'))
            node.addInput(inp1)
                .addInput(inp2)
                .addOutput(out);
        }
        else if (["linspace"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('start', "start", SocketFloat);
            var inp2 = new Rete.Input('stop', "stop", SocketFloat);
            var inp3 = new Rete.Input('num', "num", SocketFloat);
            var out = new Rete.Output('result', "result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'start'))
            inp2.addControl(new FloatControl(editor, 'stop'))
            inp3.addControl(new FloatControl(editor, 'num'))
            node.addInput(inp1)
                .addInput(inp2)
                .addInput(inp3)
                .addOutput(out);
        }
        else if (["arange"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('start', "start", SocketFloat);
            var inp2 = new Rete.Input('stop', "stop", SocketFloat);
            var inp3 = new Rete.Input('step', "step", SocketFloat);
            var out = new Rete.Output('result', "result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'start'))
            inp2.addControl(new FloatControl(editor, 'stop'))
            inp3.addControl(new FloatControl(editor, 'step'))
            node.addInput(inp1)
                .addInput(inp2)
                .addInput(inp3)
                .addOutput(out);
        }
        else if (["cos", "sin"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('x', "x", SocketFloat);
            var out = new Rete.Output('result', "result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            node.addInput(inp1)
                .addOutput(out);
        }
        else if (["argmax", "argmin"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('a', "a", SocketGeneral);
            var inp2 = new Rete.Input('axis', "axis", SocketFloat);
            var out = new Rete.Output('result', "result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            node.addInput(inp1)
                .addInput(inp2)
                .addOutput(out);
        }
        else {
            var inp1 = new Rete.Input('x', "x", SocketFloat);
            var out = new Rete.Output('result', "result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            node.addInput(inp1)
                .addOutput(out);
        }
    }

    builder(node) {
        this.init(node);
        node.createSockets = this.createSockets;
        this.createControls(node, control_callback);
        this.createSockets(node);
        return node
    }
}


// python builtin
StringComponent = createScinodeComponent({"name": "String", "catalog": "Input", "controls": [["String", "value"]], "inputs": [], "outputs": [["String", "string"]]});
IntComponent = createScinodeComponent({"name": "Int", "catalog": "Input", "controls": [["Int", "value"]], "inputs": [], "outputs": [["Int", "int"]]});
FloatComponent = createScinodeComponent({"name": "Float", "catalog": "Input", "controls": [["Float", "value"]], "inputs": [], "outputs": [["Float", "float"]]});
BoolComponent = createScinodeComponent({"name": "Bool", "catalog": "Input", "controls": [["Bool", "value"]], "inputs": [], "outputs": [["Bool", "bool"]]});
GetattrComponent = createScinodeComponent({"name": "Getattr", "catalog": "Utils", "controls": [], "inputs": [["General", "Source"], ["String", "name", {"String": "name"}]], "outputs": [["General", "result"]]});
SetattrComponent = createScinodeComponent({"name": "Setattr", "catalog": "Utils", "controls": [], "inputs": [["General", "Source"], ["String", "name", {"String": "name"}], ["General", "value"]], "outputs": [["General", "result"]]});
GetitemComponent = createScinodeComponent({"name": "Getitem", "catalog": "Utils", "controls": [], "inputs": [["General", "Source"], ["General", "index", {"Float": "index"}]], "outputs": [["General", "result"]]});
SetitemComponent = createScinodeComponent({"name": "Setitem", "catalog": "Utils", "controls": [], "inputs": [["General", "Source"], ["General", "index", {"Float": "index"}], ["General", "value"]], "outputs": [["General", "result"]]});
IndexComponent = createScinodeComponent({"name": "Index", "catalog": "Utils", "controls": [], "inputs": [["General", "source"], ["General", "value", {"Float": "value"}]], "outputs": [["General", "index"]]});
ScatterComponent = createScinodeComponent({"name": "Scatter", "catalog": "Control", "controls": [["String", "datatype", {"defaultVal": "General"}]], "inputs": [["General", "input"], ["General", "stop"]], "outputs": [["General", "result"]]});
SwitchComponent = createScinodeComponent({"name": "Switch", "catalog": "Control", "controls": [], "inputs": [["General", "input"], ["General", "switch"]], "outputs": [["General", "result"]]});
UpdateComponent = createScinodeComponent({"name": "Update", "catalog": "Control", "controls": [], "inputs": [["General", "input"], ["General", "update"]], "outputs": [["General", "result"]]});


// Test
// TestNGLComponent = createScinodeComponent({"name": "TestNGL", "catalog": "Utils", "local": true, "controls": [["NGL", "Viewer"]], "inputs": [["String", "Atoms"]], "outputs": []});


class TestNGLComponent extends ScinodeComponent {

    constructor(){
        super("NGL");
        this.catalog = 'Test';
        this.name = "TestNGL";
        this.local=true;
    }

    builder(node) {
        this.init(node);
        node.addControl(new NGLControl(this.editor, 'Viewer', node));
        var inp1 = new Rete.Input('Atoms', "Atoms", SocketGeneral);
        return node.addInput(inp1);
    }
}

//=====================================
// Python builtin
//=====================================

// Opertor
var operator_items = ["+", "-", "*", "/", "%", "**","//","==","!=",">", "<", ">=","<="]


class OperatorComponent extends ScinodeComponent {
    constructor(){
        super("Operator");
        this.catalog = 'Python';
        this.name = 'Operator'
    }

    createControls(node, callback) {
        var ctl1 = new EnumUpdateControl(this.editor, 'operator',
                    {"options": operator_items, "defaultVal": "+"},
                    callback, node);
        node.addControl(ctl1);
    }

    createSockets(node){
        var inp1 = new Rete.Input('x', "x", SocketGeneral);
        var inp2 = new Rete.Input('y', "y", SocketGeneral);
        var out = new Rete.Output('result', "result", SocketGeneral);
        inp1.addControl(new FloatControl(editor, 'x'))
        inp2.addControl(new FloatControl(editor, 'y'))
        node.addInput(inp1)
            .addInput(inp2)
            .addOutput(out);
    }

    builder(node) {
        this.init(node);
        node.createSockets = this.createSockets;
        this.createControls(node, control_callback);
        this.createSockets(node);
        return node
    }
}

//-------------------------------------
// List
var list_function_items = ["list", "append", "extend", "remove", "index", "count", "insert", "pop", "reverse"]

class ListComponent extends ScinodeComponent {
    constructor(){
        super("List");
        this.catalog = 'Python';
        this.name = 'List'
    }

    createControls(node, callback) {
        var ctl1 = new EnumUpdateControl(this.editor, 'function',
                    {"options": list_function_items, "defaultVal": "list"},
                    callback, node);
        node.addControl(ctl1);
    }

    createSockets(node){
        var inp1 = new Rete.Input('input', "input", SocketGeneral);
            var out = new Rete.Output('list', "list", SocketGeneral);
            node.addInput(inp1)
                .addOutput(out);
        if (node.data['function'] == undefined || ["list", "reverse"].includes(node.data['function'])) {
            // do nothing
        }
        else if (["append", "extend", "remove"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('value', "value", SocketGeneral);
            inp1.addControl(new FloatControl(editor, 'value'))
            node.addInput(inp1);
        }
        else if (["index", "count"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('value', "value", SocketGeneral);
            inp1.addControl(new FloatControl(editor, 'value'))
            var out = new Rete.Output('result', "result", SocketGeneral);
            node.addInput(inp1)
                .addOutput(out);
        }
        else if (["insert"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('index', "index", SocketFloat);
            var inp1 = new Rete.Input('value', "value", SocketGeneral);
            inp1.addControl(new FloatControl(editor, 'index'))
            inp2.addControl(new FloatControl(editor, 'value'))
            node.addInput(inp1)
                .addInput(inp2);
        }
        else if (["pop"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('index', "index", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'index'))
            var out = new Rete.Output('result', "result", SocketGeneral);
            node.addInput(inp1)
                .addOutput(out);
        }
    }

    builder(node) {
        this.init(node);
        node.createSockets = this.createSockets;
        this.createControls(node, control_callback);
        this.createSockets(node);
        return node
    }
}

//-------------------------------------
// Dict
var dict_function_items = ["dict", "clear", "copy", "fromkeys", "get", "items", "keys", "pop", "popitem", "setdefault", "update", "values", "__setitem__"]

class DictComponent extends ScinodeComponent {
    constructor(){
        super("Dict");
        this.catalog = 'Python';
        this.name = 'Dict'
    }

    createControls(node, callback) {
        var ctl1 = new EnumUpdateControl(this.editor, 'function',
                    {"options": dict_function_items, "defaultVal": "dict"},
                    callback, node);
        node.addControl(ctl1);
    }

    createSockets(node){
        var inp1 = new Rete.Input('input', "input", SocketGeneral);
            var out = new Rete.Output('dict', "dict", SocketGeneral);
            node.addInput(inp1)
                .addOutput(out);
        if (node.data['function'] == undefined || ["dict"].includes(node.data['function'])) {
            // do nothing
        }
        else if (["get"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('key', "key", SocketString);
            inp1.addControl(new StringControl(editor, 'key'))
            var out = new Rete.Output('result', "result", SocketGeneral);
            node.addInput(inp1)
                .addOutput(out);
        }
        else if (["pop"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('key', "key", SocketString);
            inp1.addControl(new StringControl(editor, 'key'))
            var out = new Rete.Output('result', "result", SocketGeneral);
            node.addInput(inp1)
                .addOutput(out);
        }
        else if (["update"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('value', "value", SocketGeneral);
            inp1.addControl(new FloatControl(editor, 'value'))
            node.addInput(inp1);
        }
        else if (["__setitem__"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('key', "key", SocketString);
            var inp2 = new Rete.Input('value', "value", SocketGeneral);
            inp1.addControl(new StringControl(editor, 'key'))
            inp2.addControl(new FloatControl(editor, 'value'))
            node.addInput(inp1)
                .addInput(inp2);
        }
        else if (["keys", "values", "items"].includes(node.data['function'])) {
            var out = new Rete.Output('result', "result", SocketGeneral);
            node.addOutput(out);
        }
    }

    builder(node) {
        this.init(node);
        node.createSockets = this.createSockets;
        this.createControls(node, control_callback);
        this.createSockets(node);
        return node
    }
}

var components = [
    new TestStringComponent(),
    new TestFloatComponent(),
    new TestAddComponent(),
    new TestMinusComponent(),
    new TestSqrtComponent(),
    new TestGreaterComponent(),
    new TestLessComponent(),
    new TestRangeComponent(),
    new TestEnumComponent(),
    new TestEnumUpdateComponent(),
    // python builtin
    new StringComponent(),
    new IntComponent(),
    new FloatComponent(),
    new BoolComponent(),
    //
    new GetattrComponent(),
    new SetattrComponent(),
    new GetitemComponent(),
    new SetitemComponent(),
    new IndexComponent(),
    // control
    new ScatterComponent(),
    new SwitchComponent(),
    new UpdateComponent(),
    //
    new NumpyComponent(),
    // Test
    new TestNGLComponent(),
    // Python
    new OperatorComponent(),
    new ListComponent(),
    new DictComponent(),
];

// register all nodes
components.map(c => {
    editor.register(c);
    engine.register(c);
    });
