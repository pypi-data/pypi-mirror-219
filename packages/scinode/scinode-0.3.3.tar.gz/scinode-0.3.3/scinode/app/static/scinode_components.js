var CustomNode = {
    template: `<div class="node" :class="[selected(), node.name] | kebab">
    <div class="title">{{node.label}}<span style="float:right; font-size: 16px" class="fa fa-lg" :class="[node.icon] | kebab"></span></div>
    <!-- Outputs-->
    <div class="output" v-for="output in outputs()" :key="output.key">
      <div class="output-title">{{output.name}}</div>
      <Socket v-socket:output="output" type="output" :socket="output.socket"></Socket>
    </div>
    <!-- Controls-->
    <div class="control" v-for="control in controls()" v-control="control"></div>
    <!-- Inputs-->
    <div class="input" v-for="input in inputs()" :key="input.key">
      <Socket v-socket:input="input" type="input" :socket="input.socket"></Socket>
      <div class="input-title" v-show="!input.showControl()">{{input.name}}</div>
      <div class="input-control" v-show="input.showControl()" v-control="input.control"></div>
    </div>
  </div>`,
  mixins: [VueRenderPlugin.default.mixin],
  components: {
      Socket: VueRenderPlugin.default.Socket
    }
  }


class ScinodeComponent extends Rete.Component {

    constructor(name){
        super(name);
        this.data.component = CustomNode;
    }
    // create controls
    createControls(node) {};
    // create node input and output sockets
    createSockets(node) {};

    init(node) {
        node.label = node.name + node.id;
        node.uuid = uuid4();
        node.state = 'CREATED';
        node.action = 'NONE';
        node.icon = "fa-gear";
        node.setMeta({
        "identifier": this.name,
        "worker_name": '',
        "platform": 'rete',
        "local": this.local,
        });
        node.executor = {"path": "scinode.executors.built_in",
          "name": "PropertyToSocket",
          "type": "class",
          };
        // override the toJSON method
        node.builtin_toJSON = node.toJSON
        node.toJSON = function toJSON() {
            var data = this.builtin_toJSON();
            data['label'] = this.label;
            data['uuid'] = this.uuid;
            data['metadata'] = this.meta;
            data['executor'] = this.executor;
            data['controls'] = {};
            data['description'] = "";
            this.controls.forEach(function(control, key) {
                data['controls'][key] = {'name': control.key, 'value': data["data"][key], 'type': control.type}
            })
            this.inputs.forEach(function(input, key) {
                console.log(input.name);
                delete data["inputs"][input.name]["connections"];
                if (input.uuid == undefined) {
                    input.uuid = uuid4();
                }
                let control = input.control;
                if (control != undefined) {
                    data['controls'][key] = {'name': control.key, 'value': data["data"][key], 'type': control.type}
                }
                console.log(input.name);
            })
            this.outputs.forEach(function(output, key) {
                delete data["outputs"][output.name]["connections"];
                if (output.uuid == undefined) {
                    output.uuid = uuid4();
                }
            })
            delete data["data"];
            return data;
        }
    }
    builder(node) {
        function setControls(node) {
            // control, for the enum control with callback
            for ( let [key, control] of node.controls) {
                if (node.data[key] != undefined) {
                    control.setValue(node.data[key]);
                }
            }
        };

        this.init(node);
        this.createControls(node);
        this.createSockets(node);
        // setControls(node);
        return node
    }
}


// I want to create a new component inside a function to extend the ScinodeComponent class. This new component will has a new name and a new catalog, and new controls, inputs and outputs base on the input data.

function createControl(cdata) {
    // if the type is in the system, use the system control
    // if not, use a general control
    // if the identifier class is not defined, use the general control
    // get the global variable of the nodejs
    var controlClass = scinode_controls[cdata[0]]
    if (controlClass == undefined) {
        controlClass = GeneralControl;
    }
    // if cdata's length is 3, it has data
    console.log("cdata: ", cdata, controlClass);
    if (cdata.length == 3) {
        return new controlClass(this.editor, cdata[1], cdata[2]);
    }
    else {
        return new controlClass(this.editor, cdata[1])
    }
}

function createScinodeComponent(ndata) {

    class AutoCreatedComponent extends ScinodeComponent {

        constructor(){
            super(ndata.name);
            this.catalog = ndata.catalog;
            this.name = ndata.name;
            // local is false if ndata.local is undefined
            this.local = ndata.local || false;
        }
        createControls(node) {
            // loop the ntdata.controls and create controls
            for (let i = 0; i < ndata.controls.length; i++) {
                node.addControl(createControl(ndata.controls[i]));
            }
        }
        createSockets(node) {
            // loop the ndata.inputs and create inputs
            for (let i = 0; i < ndata.inputs.length; i++) {
                // if the type is in the system, use the system socket
                // if not, use a general socket
                // get the global variable of the nodejs
                var socketClass = scinode_sockets[ndata.inputs[i][0]];
                if (socketClass == undefined) {
                    socketClass = SocketGeneral;
                }
                var inp = new Rete.Input(ndata.inputs[i][1], ndata.inputs[i][1], socketClass);
                // if the socket's length is 3, it has control
                if (ndata.inputs[i].length == 3) {
                    inp.addControl(createControl(ndata.inputs[i][2]));
                }
                node.addInput(inp);
            }
            // loop the ndata.outputs and create outputs
            for (let i = 0; i < ndata.outputs.length; i++) {
                // if the type is in the system, use the system socket
                // if not, use a general socket
                var socketClass = scinode_sockets[ndata.outputs[i][0]];
                if (socketClass == undefined) {
                    socketClass = SocketGeneral;
                }
                var out = new Rete.Output(ndata.outputs[i][1], ndata.outputs[i][1], socketClass);
                node.addOutput(out);
            }
        }
    }
    return AutoCreatedComponent;
}

class TemplateComponent extends ScinodeComponent {

    constructor(){
        super("Template");
        this.name = "Template";
        this.catalog = 'Template';
    }

    builder(node) {
        this.init(node);
        node.executor = {"path": "scinode.executors.built_in",
          "name": "PropertyToSocket",
          "type": "class",
          };
        var inp1 = new Rete.Input('input1', "input1", SocketFloat);
        var inp2 = new Rete.Input('input2', "input2", SocketFloat);
        var out1 = new Rete.Output('output', "output", SocketFloat);

        node.addControl(new FloatControl(this.editor, 'control1'));
        node.addControl(new StringControl(this.editor, 'control2'));
        inp1.addControl(new FloatControl(this.editor, 'input1'));
        node.addInput(inp1);
        node.addInput(inp2);
        node.addOutput(out1);
        node.kwargs = ['input'];
        return node
    }
}
