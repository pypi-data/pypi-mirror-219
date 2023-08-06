
class TemplateTestComponent extends ScinodeComponent {

    constructor(){
        super("TemplateTest");
        this.catalog = "Template";
        this.name = "Test";
    }

    builder(node) {
        this.init(node);
        node.metadata.args = ['text', 'float', 'enum', 'bool', 'matrix'];
        node.metadata.kwargs = ['input1', 'intpu2'];

        node.addControl(new StringControl(this.editor, "text", {"name": "text", "type": "String", "defaultVal": "abc"}));
        node.addControl(new FloatControl(this.editor, "float", {"name": "float", "type": "Float", "defaultVal": 10}));
        node.addControl(new EnumControl(this.editor, "enum", {"name": "enum", "type": "Enum", "defaultVal": "a", "options": ["a", "b", "c"]}));
        node.addControl(new BoolControl(this.editor, "bool", {"name": "bool", "type": "Bool", "defaultVal": true}));
        node.addControl(new FloatMatrixControl(this.editor, "matrix", {"name": "matrix", "type": "FloatMatrix", "defaultVal": [1, 2, 3, 4, 5, 6], "size": [2, 3]}));
        node.addControl(new FloatControl(this.editor, "input1", {"defaultVal": 0, "type": "Float", "name": "input1"}));
        node.addControl(new FloatVectorControl(this.editor, "input2", {"defaultVal": [1, 2, 3], "size": 3, "type": "FloatVector", "name": "input2"}));
        var inp0 = new Rete.Input("input1","input1", SocketFloat);
        node.addInput(inp0);
        var inp1 = new Rete.Input("input2","input2", SocketFloatVector);
        node.addInput(inp1);
        var out0 = new Rete.Output("Output","Output", SocketFloat);
        node.addOutput(out0);
        node.executor = {"path": "numpy", "name": "add", "type": "function"};

        return node
    }
}
class TemplateTestnglComponent extends ScinodeComponent {

    constructor(){
        super("TemplateTestngl");
        this.catalog = "Template";
        this.name = "Testngl";
    }

    builder(node) {
        this.init(node);
        node.metadata.args = [];
        node.metadata.kwargs = ['ngl', 'input2'];

        node.addControl(new NGLControl(this.editor, "ngl", {"name": "ngl", "type": "NGL"}));
        node.addControl(new FloatVectorControl(this.editor, "input2", {"defaultVal": [1, 2, 3], "size": 3, "type": "FloatVector", "name": "input2"}));
        var inp0 = new Rete.Input("input2","input2", SocketFloatVector);
        node.addInput(inp0);
        var out0 = new Rete.Output("Output","Output", SocketFloat);
        node.addOutput(out0);
        node.executor = {"path": "numpy", "name": "add", "type": "function"};

        return node
    }
}
class TemplateTestNGLComponent extends ScinodeComponent {

    constructor(){
        super("TemplateTestNGL");
        this.catalog = "Template";
        this.name = "TestNGL";
    }

    builder(node) {
        this.init(node);
        node.metadata.args = [];
        node.metadata.kwargs = ['ngl', 'input2'];

        node.addControl(new NGLControl(this.editor, "ngl", {"name": "ngl", "type": "NGL"}));
        node.addControl(new FloatVectorControl(this.editor, "input2", {"defaultVal": [1, 2, 3], "size": 3, "type": "FloatVector", "name": "input2"}));
        var inp0 = new Rete.Input("input2","input2", SocketFloatVector);
        node.addInput(inp0);
        var out0 = new Rete.Output("Output","Output", SocketFloat);
        node.addOutput(out0);
        node.executor = {"path": "numpy", "name": "add", "type": "function"};

        return node
    }
}
class TemplateTestNGL2Component extends ScinodeComponent {

    constructor(){
        super("TemplateTestNGL2");
        this.catalog = "Template";
        this.name = "TestNGL2";
    }

    builder(node) {
        this.init(node);
        node.metadata.args = [];
        node.metadata.kwargs = ['ngl', 'input2'];

        node.addControl(new NGLControl(this.editor, "ngl", {"name": "ngl", "type": "NGL"}));
        node.addControl(new FloatVectorControl(this.editor, "input2", {"defaultVal": [1, 2, 3], "size": 3, "type": "FloatVector", "name": "input2"}));
        var inp0 = new Rete.Input("input2","input2", SocketFloatVector);
        node.addInput(inp0);
        var out0 = new Rete.Output("Output","Output", SocketFloat);
        node.addOutput(out0);
        node.executor = {"path": "numpy", "name": "add", "type": "function"};

        return node
    }
}
class TemplateTestPlotyComponent extends ScinodeComponent {

    constructor(){
        super("TemplateTestPloty");
        this.catalog = "Template";
        this.name = "TestPloty";
    }

    builder(node) {
        this.init(node);
        node.metadata.args = ['text'];
        node.metadata.kwargs = ['input1', 'intpu2'];

        node.addControl(new PlotlyBasicChartControl(this.editor, "text", {"name": "text", "type": "PlotlyBasicChart", "defaultVal": "abc"}));
        node.addControl(new FloatControl(this.editor, "input1", {"defaultVal": 0, "type": "Float", "name": "input1"}));
        node.addControl(new FloatVectorControl(this.editor, "input2", {"defaultVal": [1, 2, 3], "size": 3, "type": "FloatVector", "name": "input2"}));
        var inp0 = new Rete.Input("input1","input1", SocketFloat);
        node.addInput(inp0);
        var inp1 = new Rete.Input("input2","input2", SocketFloatVector);
        node.addInput(inp1);
        var out0 = new Rete.Output("Output","Output", SocketFloat);
        node.addOutput(out0);
        node.executor = {"path": "numpy", "name": "add", "type": "function"};

        return node
    }
}
var json_components = [new TemplateTestComponent(),
new TemplateTestnglComponent(),
new TemplateTestNGLComponent(),
new TemplateTestNGL2Component(),
new TemplateTestPlotyComponent(),
];
