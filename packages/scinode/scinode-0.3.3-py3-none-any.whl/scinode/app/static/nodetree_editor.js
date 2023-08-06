editor.use(AutoArrangePlugin.default, { margin: {x: 50, y: 50 }, depth: 100 });
// load nodetree_data
console.log("input nodetree_data: ", nodetree_data)
// register the undifined node components
// loop nodes dict in the nodetree_data, if the node not in the editor, register it

for (let [key, node] of Object.entries(nodetree_data["nodes"])) {
  let node_name = node["constructor"]["name"];
  if (!editor.components.has(node_name)) {
    console.log("register node: ", node_name);
    console.log("node: ", node["constructor"]);
  // create new node component use the node constructor
    NewComponent = createScinodeComponent(node["constructor"]);
    editor.register(new NewComponent());
  }
}
//
editor
  .fromJSON(nodetree_data)
  .then(() => editor.trigger("process"))
  .then(loadNodetreeData(nodetree_data))
  .then(setStateColor());

// update node UI for selected nodes
editor.on("nodeselected", setSelectNodeUI);

editor.view.resize();
AreaPlugin.zoomAt(editor);
editor.trigger("process");

async function loadNodetreeData(nodetree_data) {
  await engine.abort();
  console.log("loadNodetreeData");
  editor.index = nodetree_data["index"];
  editor.name = nodetree_data["name"];
  editor.uuid = nodetree_data["uuid"];
  editor.state = nodetree_data["state"];
  editor.action = nodetree_data["action"];
  editor.meta.worker_name = nodetree_data["metadata"]["worker_name"];
  editor.meta.parent = nodetree_data["metadata"]["parent"];
  editor.meta.parent_node = nodetree_data["metadata"]["parent_node"];
  editor.meta.scatter_node = nodetree_data["metadata"]["scatter_node"];
  editor.meta.scattered_label = nodetree_data["metadata"]["scattered_label"];
  // console.log("Editor: ", editor)
  setNodes(nodetree_data);
  setNodetreeUI(nodetree_data);
}

function setNodes(nodetree_data) {
  // set metadata data to Node
  // uuid, nodetree_uuid
  console.log("nodes: ", editor.nodes.length);
  console.log("setNode: ", nodetree_data['nodes']);
  for (let i = 0; i < editor.nodes.length; i++) {
    console.log("i: ", i)
    setNode(editor.nodes[i], nodetree_data["nodes"][editor.nodes[i].id]);
  }
}

function setNode(node, ndata){
  // set node use the data from database
  node.label = ndata["label"];
  node.uuid = ndata["uuid"];
  // node.counter = nodetree_data['nodes'][node.id]['counter'];
  // console.log("set node state: ", i, ndata["state"])
  node.name = ndata["name"];
  node.state = ndata["state"];
  node.icon = ndata["metadata"]["icon"];
  node.meta.worker_name =
    ndata["metadata"]["worker_name"];
  node.executor = ndata["executor"];
  // inputs
  console.log("inputs", ndata["inputs"])
  node.update();
  for ( let [key, input] of node.inputs) {
    // console.log("input: ", input.name, "key", key)
    if (ndata["inputs"][key] != undefined) {
      // console.log("set input uuid: ", ndata["inputs"][key]["uuid"])
      input.uuid = ndata["inputs"][key]["uuid"];
      if (input.control != null) {
        input.control.setValue(ndata["data"][key]);
      }
      console.log("key: ", key, "uuid: ", input.uuid)
    }
  }
  // outputs
  console.log("outputs", ndata["outputs"]);
  for ( let [key, output] of node.outputs) {
    console.log("output: ", output.name, "key", key)
    output.uuid = ndata["outputs"][key]["uuid"];
  }
}

function setNodeControl(node, cdata){
  // set node control use the data from database
  // console.log("id: ", node.id);
  // console.log("cdata: ", cdata);
  // controls
  for ( let [key, control] of node.controls) {
    // console.log("control: ", control.key)
    if (cdata[key] != undefined) {
        control.setValue(cdata[key]);
      }
    }
  // inputs
  for ( let [key, input] of node.inputs) {
    // console.log("input: ", input.name)
    if (cdata[key] != undefined) {
      if (input.control != null) {
        input.control.setValue(cdata[key]);
      }
    }
  }
}

function setNodetreeUI(nodetree_data) {
  // update html element based on data
  document.getElementById("nodetree_name").value = editor.name;
  document.getElementById("nodetree_worker_name").value =
    editor.meta.worker_name;
  document.getElementById("nodetree_uuid").value = editor.uuid;
  document.getElementById("nodetree_state").value = editor.state;
  document.getElementById("nodetree_action").value = editor.action;
}

function setNodetreeProps(data) {
  // set editor data by html element
  for (var key in data) {
    editor[key] = data[key];
  }
}

function setSelectedNodeProps(data) {
  // set editor data by html element
  var node = editor.selected.list[0];
  for (var key in data) {
    if (node.meta.hasOwnProperty(key)) {
      node.meta[key] = data[key];
    }
    else {
      node[key] = data[key];
    }
  }
  node.update();
}

async function nodetree_post(data, url) {
  // post nodetree data to app
  // console.log("post Nodetree: ", data);
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  response.json().then((data) => {
    alert(data['message']);
    // console.log(url + "/" + data["uuid"])
    // redirect page  mh
    if (window.location.href.split("/").slice(-1)[0] != data["uuid"]) {
      window.location.href = url + "/" + data["uuid"];
    }
  });
  return data;
}

async function nodetree_get(url) {
  // get nodetree data to app
  const response = await fetch(url)
    .then((response) => response.json())
    .then((data) => {
      var nodetree_data = data["nodetree_data"];
      // console.log("nodetree_get: ",nodetree_data);
      return nodetree_data;
    });
}

function saveNodetree() {
  // Launch nodetree
  var data = editor.toJSON();
  // post nodetree data
  data = nodetree_post(data, "/nodetrees");
}


function launchNodetree() {
  if (confirm("Are You Sure to launch this Nodetree?")) {
    // Save nodetree
    nodetree_push_message(editor.uuid+",nodetree,action:LAUNCH")
  }
}

function saveAsTemplate() {
  // Launch nodetree
  var data = editor.toJSON();
  // post nodetree data
  nodetree_post(data, "/templates");
}

function resetNodetree() {
  if (confirm("Are You Sure to reset this Nodetree?")) {
    // reset nodetree
    msg = editor.uuid+",nodetree," + "action:RESET"
    nodetree_push_message(msg);
  }
}

function setSelectNodeUI() {
  // update html element based on data
  if (editor.selected.list.length > 0) {
    document.getElementById("node_uuid").value = editor.selected.list[0].uuid;
    document.getElementById("node_name").value = editor.selected.list[0].label;
    document.getElementById("node_worker_name").value =
      editor.selected.list[0].meta.worker_name;
    document.getElementById("node_state").value = editor.selected.list[0].state;
    document.getElementById('node_edit').value = "";
  }
}

function actionSelectedNode(action) {
  // reset selected node
  if (confirm("Are You Sure to " + action + " " + editor.selected.list.length +" nodes?")) {
    for (let i = 0; i < editor.selected.list.length; i++) {

      msg = editor.uuid+",node," + editor.selected.list[i].label + ":action:" + action
      nodetree_push_message(msg);
  }
    // editor.selected.list[i].state = "CREATED";
    // editor.selected.list[i].meta.worker_name = "";
    // editor.selected.list[i].meta.counter = 0;
    // setSelectNodeUI();
  }
}

function editSelectedNodeData() {
  fetch('/nodes/edit/'+editor.selected.list[0].uuid)
			.then(response => response.text())
			.then(data => {
				// insert the fetched HTML data into the section
				document.getElementById('node_edit').value = data;
			})
			.catch(error => console.error(error));
}

async function saveSelectedNodeData() {
  // post node data to app
  var node_edit = document.getElementById('node_edit').value;
  var data = {"node_edit": node_edit,
              "name": editor.selected.list[0].name,
              "uuid": editor.selected.list[0].uuid,
            "nodetree_uuid": editor.uuid}
  console.log("post Node data: ", data);
  var url = '/nodes/edit/'+editor.selected.list[0].uuid;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  response.json().then((data) => {
    console.log(data);
    setNodeControl(editor.selected.list[0], data["node_data"]);
    alert(data['message']);
  });
}

async function nodetree_push_message(data) {
  // post nodetree message to app
  console.log("Nodetree push message: ", data);
  console.log("Nodetree uuid: ", editor.uuid);
  const response = await fetch("/scheduler/", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  response.json().then((data) => {
    console.log(data);
  });
}

function removeStateTag(item) {
  item.classList.remove("finished");
  item.classList.remove("failed");
  item.classList.remove("paused");
  item.classList.remove("running");
  item.classList.remove("waiting");
  item.classList.remove("created");
}


async function setNodeState(states) {
  await engine.abort();
  // console.log(states)
  if (Object.keys(states).length == 0) {
    return;
  }
  // console.log("states: ", states)
  for (let i = 0; i < editor.nodes.length; i++) {
    editor.nodes[i].state = states[editor.nodes[i].label]["state"];
  }
}


async function setStateColor() {
  await engine.abort();
  let s = document.getElementById("stateSwitchCheck");
  var titles = document.querySelectorAll(".node");
  if (s.checked) {
    for (let i = 0; i < editor.nodes.length; i++) {
      // remove old
      //   console.log("i: ", i)
      removeStateTag(titles[i]);
      titles[i].classList.add(editor.nodes[i].state.toLowerCase());
    }
  } else {
    for (let i = 0; i < editor.nodes.length; i++) {
      removeStateTag(titles[i]);
    }
  }
}

async function refreshNodetree() {
  // reload nodetree
  if (editor.uuid != "") {
    const response = await fetch("/nodetrees/api/" + editor.uuid)
      .then((response) => response.json())
      .then((data) => {
        var nodetree_data = data["nodetree_data"];
        // console.log("nodetree_data: ", nodetree_data);
        editor
          .fromJSON(nodetree_data)
          .then(() => editor.trigger("process"))
          .then(loadNodetreeData(nodetree_data))
          .then(setStateColor());
      });
  }
}

async function refreshNodeState() {
  // reload nodetree
  if (editor.uuid != "") {
    const response = await fetch("/nodetrees/state/" + editor.uuid)
      .then((response) => response.json())
      .then((data) => {
        // console.log("states: ", data);
        setNodeState(data)
          .then(setStateColor());
      });
  }
}

function arrangeNodetree() {
  console.log('Arranging...')
  editor.trigger('arrange');
}
