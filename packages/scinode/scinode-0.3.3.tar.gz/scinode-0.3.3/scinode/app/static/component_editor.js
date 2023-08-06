/*
Editor for component.
Only on component in the Editor, so we don't need connection and menu plugin.

Step:
1. initial a Editor
2. register TemplateComponent
3. add a Template node
4. Set node using json data, e.g. change name, catalog, executor, controls, inputs and outputs.
5. Set UI form with node data
6. modify UI
7. get UI data
8. preview, update ndoe data with UI data
9. save to database
*/

var container = document.querySelector('#rete');
// var editor = new Rete.NodeEditor('scinode@0.1.0', container);
var editor = new ScinodeEditor('scinode@0.1.0', container);
editor.use(VueRenderPlugin.default);
// editor.use(MinimapPlugin);
var engine = new Rete.Engine('scinode@0.1.0');
var components = [new TemplateComponent()];
components.map(c => {
    editor.register(c);
    engine.register(c);
});

// });
editor.view.resize();
AreaPlugin.zoomAt(editor);
editor.trigger('process');

// console.log(nodetree_data)

add_node()
    .then(() => editor.trigger('process'))
    .then(setNode(component_json))
    .then(setUI);


async function add_node() {
    var n1 = await components[0].createNode();
    n1.position = [-100, -100];
    editor.addNode(n1);
    console.log("add_node: ", n1);
    // console.log("add_node: ", editor.nodes[0]);
}

async function setNode(component_json) {
    await engine.abort();
    editor.nodes[0].data = {};
    editor.nodes[0].controls.clear();
    editor.nodes[0].inputs.clear();
    editor.nodes[0].outputs.clear();
    // console.log("setNode, component_json: ", component_json);
    if (component_json.hasOwnProperty('real_name')) {
        editor.nodes[0].name = component_json['real_name'];
    }
    else {
        editor.nodes[0].name = component_json['name'];
    }
    editor.nodes[0].meta.catalog = component_json['metadata']['catalog'];
    editor.nodes[0].meta.args = component_json['metadata']['args'];
    editor.nodes[0].meta.kwargs = component_json['metadata']['kwargs'];
    editor.nodes[0].executor = component_json['executor'];
    // console.log(text)
    // set control
    await editor.nodes[0].update();
    var controls = component_json['controls'];
    for (let i = 0; i < controls.length; i++) {
        let data = controls[i];
        console.log("setNode, control: ", data)
        editor.nodes[0].addControl(new scinode_controls[data['type']](editor, data['name'], data));
    }
    // set input
    var inputs = component_json['inputs'];
    for (let i = 0; i < inputs.length; i++) {
        let data = inputs[i];
        let input = new Rete.Input(data['name'], data['name'], new Rete.Socket(data['type']))
        if (data.hasOwnProperty('control') && data['control']['type'] != 'None') {
            let control = data['control'];
            // console.log("control data: ", control)
            input.addControl(new scinode_controls[control['type']](editor, data['name'], control))
        }
        editor.nodes[0].addInput(input)
    }
    // set output
    var outputs = component_json['outputs'];
    for (let i = 0; i < outputs.length; i++) {
        let data = outputs[i];
        editor.nodes[0].addOutput(new Rete.Output(data['name'], data['name'], new Rete.Socket(data['type'])))
    }
    let node = editor.nodes[0];
    await node.update();
}


async function previewComponent() {
    var component_json = getUI();
    setNode(component_json);
}

async function saveComponent() {
    var component_json = getUI();
    save_component(component_json);
    // console.log(text)
}

function getUI() {
    component_json = {"metadata": {}, "controls": [], "inputs": [], "outputs": [], "executor": {}};
    component_json['name'] = document.getElementById('componentName').value;
    component_json['uuid'] = document.getElementById('componentUUID').value;
    component_json['metadata']['catalog'] = document.getElementById('componentCatalog').value;
    let args = document.getElementById('componentArgs').value.replace(/\s+/g, '');
    let kwargs = document.getElementById('componentKwargs').value.replace(/\s+/g, '');
    if (args=='') {
        component_json['metadata']['args'] = [];
    }
    else {
        component_json['metadata']['args'] = args.split(",");
    }
    if (kwargs=='') {
        component_json['metadata']['kwargs'] = [];
    }
    else {
        component_json['metadata']['kwargs'] = kwargs.split(",");
    }
    component_json['executor']['path'] = document.getElementById('executorPath').value;
    component_json['executor']['name'] = document.getElementById('executorName').value;
    if (document.getElementById('executorCheck').checked) {
        component_json['executor']['type'] = "class";
    }
    else {
        component_json['executor']['type'] = "function";
    }
    // read control
    var controls = document.getElementById('tbody-control').getElementsByClassName("row-item");
    for (let i = 0; i < controls.length; i++) {
        let data = controls[i].getElementsByTagName('input');
        let textarea = controls[i].getElementsByTagName('textarea');
        let select = controls[i].getElementsByClassName('select-control');
        if (data[0].value == '') {
            alert("Please input a name for the " + (i+1) + "th control.")
            break;
        }
        var control = {"name": data[0].value,
                        "type": select[0].value,}
        if (textarea[0].value.trim() == '') {
            textarea[0].value = "{}";
        }
        control = Object.assign(control, JSON.parse(textarea[0].value));
        component_json['controls'].push(control);
    }
    // read input
    var inputs = document.getElementById('tbody-input').getElementsByClassName("row-item");
    for (let i = 0; i < inputs.length; i++) {
        let data = inputs[i].getElementsByTagName('input');
        let textarea = inputs[i].getElementsByTagName('textarea');
        if (data[0].value == '') {
            alert("Please input a name for the " + (i+1) + "th input socket.")
            break;
        }
        var input = {"name": data[0].value,
                    "type": data[1].value,
                    }
        if (textarea[0].value.trim() == '') {
            textarea[0].value = "{}";
        }
        let select = inputs[i].getElementsByClassName('select-input');
        input['control'] = JSON.parse(textarea[0].value);
        input['control']['type'] = select[0].value;
        component_json['inputs'].push(input);
    }
    // read output
    var outputs = document.getElementById('tbody-output').getElementsByClassName("row-item");
    for (let i = 0; i < outputs.length; i++) {
        let data = outputs[i].getElementsByTagName('input');
        if (data[0].value == '') {
            alert("Please input a name for the " + (i+1) + "th output socket.")
            break;
        }
        var output = {"name": data[0].value,
                        "type": data[1].value}
        component_json['outputs'].push(output);
    }
    console.log("component_json: ", component_json)
    return component_json;
}


async function setUI() {
    // set metadata data to Node
    await engine.abort();
    if (nodetree_data['nodes'][1].hasOwnProperty('uuid')) {
        document.getElementById('componentUUID').value = nodetree_data['nodes'][1]['uuid'];
    }
    document.getElementById('componentName').value = editor.nodes[0]['name'];
    document.getElementById('componentCatalog').value = editor.nodes[0].meta['catalog'];
    document.getElementById('componentArgs').value = editor.nodes[0].meta['args'];
    document.getElementById('componentKwargs').value = editor.nodes[0].meta['kwargs'];
    document.getElementById('executorPath').value = editor.nodes[0]['executor']['path'];
    document.getElementById('executorName').value = editor.nodes[0]['executor']['name'];
    if (editor.nodes[0]['executor']['type'] == 'class') {
        document.getElementById('executorCheck').checked = true;
    }
    else {
        document.getElementById('executorCheck').checked = false;
    }
    // set controls
    var i = 0;
    editor.nodes[0].controls.forEach(function(value, key) {
        addControlUI();
        console.log("add ui control: ", i)
        var input = document.getElementById('tbody-control').getElementsByTagName('input');
        var textarea = document.getElementById('tbody-control').getElementsByTagName('textarea');
        input[i].value = value.key;
        delete value.data['name'];
        delete value.data['type'];
        textarea[i].value = JSON.stringify(value.data);
        var select = document.getElementsByClassName("select-control");
        select[i].value = scinode_controls_key[value.constructor.name];
        i = i + 1;
    });
    // set inputs
    var i = 0;
    editor.nodes[0].inputs.forEach(function(value, key) {
        addInputUI();
        var input = document.getElementById('tbody-input').getElementsByTagName('input');
        var textarea = document.getElementById('tbody-input').getElementsByTagName('textarea');
        input[i*2].value = value.name;
        input[i*2 + 1].value = value.socket.name;
        if (value.control) {
            var select = document.getElementsByClassName("select-input");
            select[i].value = scinode_controls_key[value.control.constructor.name];
            delete value.control.data['name'];
            delete value.control.data['type'];
            textarea[i].value = JSON.stringify(value.control.data);
        }
        i = i + 1;
    });
    // set outputs
    var i = 0;
    editor.nodes[0].outputs.forEach(function(value, key) {
        addOutputUI();
        var input = document.getElementById('tbody-output').getElementsByTagName('input');
        input[i*2].value = value.name;
        input[i*2 + 1].value = value.socket.name;
        i = i + 1;
    });
}


async function save_component(component_data) {
    // post nodetree component_data to app
    if (component_data.hasOwnProperty('uuid') && component_data['uuid'] != '') {
        method = 'PUT';
        url = "/components/" + component_data['uuid'];
    }
    else {
        method = 'POST';
        url = "/components";
    }
    console.log(method, url)
    const response = await fetch(url, {
    method: method,
    headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    },
    body: JSON.stringify(component_data),
    });
    response.json().then(data => {
    console.log(data);
    if (data['success']) {
        window.location.href = '/components/' + data['uuid'];
    }
    else {
        alert(data['message']);
    }
    });
}

function addControl() {
    var id = Math.random().toString(36).slice(2, 7);
    editor.nodes[0].addControl(new FloatControl(this.editor, id))
    addControlUI();
}

function addControlUI () {
    //
    // Adding a row inside the tbody.
    $("#tbody-control").append(`<tr class="row-item">
         <td class="row-index text-center">
            <input type="text" class="form-control" id="itemName", placeholder="Name">
         </td>
         <td class="text-center">
            <select class="select-control">
                <option value="Float">Float</option>
                <option value="String">String</option>
                <option value="Bool">Bool</option>
                <option value="FloatVector">FloatVector</option>
                <option value="FloatMatrix">FloatMatrix</option>
                <option value="Color">Color</option>
                <option value="File">File</option>
                <option value="Enum">Enum</option>
                <option value="PlotlyBasicChart">PlotlyBasicChart</option>
                <option value="NGL">NGL</option>


                </select>
         </td>
         <td class="row-index text-center">
            <textarea rows=3 id="itemDefaultVal" placeholder='Add metadata: \{"defaultVal": 0\}.'></textarea>
         </td>
          <td class="text-center">
            <button class="btn btn-sm btn-warning remove"
              type="button">Remove</button>
            </td>
          </tr>`);
}

function addInput() {
    var id = Math.random().toString(36).slice(2, 7);
    editor.nodes[0].addInput(new Rete.Input(id, id, new Rete.Socket('SocketFloat')))
    addInputUI();
}

function addInputUI () {
    //
    // Adding a row inside the tbody.
    $("#tbody-input").append(`<tr class="row-item">
         <td class="row-index text-center">
            <input type="text" class="form-control" id="itemName"
                placeholder="Name">
         </td>
         <td class="text-center">
            <input type="text" class="form-control" id="itemType"
                placeholder="Type">
         </td>
         <td class="text-center">
            <select class="select-input">
                <option value="None">None</option>
                <option value="Float">Float</option>
                <option value="String">String</option>
                <option value="Bool">Bool</option>
                <option value="FloatVector">FloatVector</option>
                <option value="FloatMatrix">FloatMatrix</option>
                <option value="Color">Color</option>
                <option value="File">File</option>
                <option value="Enum">Enum</option>
                <option value="NGL">NGL</option>
                </select>
         </td>
         <td class="row-index text-center">
            <textarea id="itemDefaultVal" rows=3 placeholder='Add metadata: \{"defaultVal": 0, "options": ["a", "b"], "size": [1, 2]\}.'></textarea>
         </td>
          <td class="text-center">
            <button class="btn btn-sm btn-warning remove"
              type="button">Remove</button>
            </td>
          </tr>`);
}

function addOutput() {
    var id = Math.random().toString(36).slice(2, 7);
    editor.nodes[0].addOutput(new Rete.Output(id, id, new Rete.Socket('SocketFloat')));
    addOutputUI();
}

function addOutputUI () {
    //
    // editor.nodes[0].addOutput(new Rete.Output("name", "name", new Rete.Socket('SocketFloat')))
    // Adding a row inside the tbody.
    $("#tbody-output").append(`<tr class="row-item">
         <td class="row-index text-center">
            <input type="text" class="form-control" id="itemName"
                placeholder="Name">
         </td>
         <td class="text-center">
            <input type="text" class="form-control" id="itemType"
                placeholder="Type">
         </td>
          <td class="text-center">
            <button class="btn btn-sm btn-warning remove"
              type="button">Remove</button>
            </td>
          </tr>`);
}

function removeItem () {
$(this).closest('tr').remove();
}


function build_node_from_json() {

}
