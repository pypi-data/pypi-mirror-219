var VueGeneralControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal'],
  template: '<div>\
              <label class="control-label">{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
              <input class="control-input" type="text" :readonly=true :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
            </div>',
  data() {
    return {
      value: '',
    }
  },
  methods: {
    change(e){
      this.value = e.target.value;
      this.update();
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, this.value)
    }
  },
  mounted() {
    let val = this.getData(this.ikey);
    if (val === undefined) {
      this.value =  this.defaultVal === undefined ? "": this.defaultVal ;
      this.update()
    }
    else {
      this.value = val
    }
  }
}

class GeneralControl extends Rete.Control {

  constructor(emitter, key, data={}, readonly) {
    super(key);
    this.type = 'General';
    this.component = VueGeneralControl;
    this.data = data;
    console.log("General data: ", this.data)
    this.props = { emitter, ikey: key, readonly,
      defaultVal: this.data['defaultVal']};
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}

var VueStringControl = {
    props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal'],
    template: '<div>\
                <label class="control-label">{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
                <input class="control-input" type="text" :readonly="readonly" :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
              </div>',
    data() {
      return {
        value: '',
      }
    },
    methods: {
      change(e){
        this.value = e.target.value;
        this.update();
      },
      update() {
        if (this.ikey)
          this.putData(this.ikey, this.value)
      }
    },
    mounted() {
      let val = this.getData(this.ikey);
      if (val === undefined) {
        this.value =  this.defaultVal === undefined ? "": this.defaultVal ;
        this.update()
      }
      else {
        this.value = val
      }
    }
  }

class StringControl extends Rete.Control {

    constructor(emitter, key, data={}, readonly) {
      super(key);
      this.type = 'String';
      this.component = VueStringControl;
      this.data = data;
      console.log("String data: ", this.data)
      this.props = { emitter, ikey: key, readonly,
        defaultVal: this.data['defaultVal']};
    }

    setValue(val) {
      this.vueContext.value = val;
    }
}


var VueEnumControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal', 'options'],
  template: '<div>\
              <label class="control-label" style="width:20%">{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
              <select class="select-input" type="text" style="width:70%"\
                :readonly="readonly" :value="value" @input="change($event)" \
                @dblclick.stop="" @pointerdown.stop="" @pointermove.stop="">\
                <option v-for="option in options" :value=[option]>{{ option }}<option>\
              </select>\
            </div>',
  data() {
    return {
      value: '',
    }
  },
  methods: {
    change(e){
      this.value = e.target.value;
      this.update();
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, this.value)
      // this.emitter.trigger('process');
      }
  },
  mounted() {
    let val = this.getData(this.ikey);
      if (val === undefined) {
        this.value =  this.defaultVal === undefined ? 0: this.defaultVal ;
        this.update()
      }
      else {
        this.value = val
      }
  }
}

class EnumControl extends Rete.Control {

  constructor(emitter, key, data = {}, readonly) {
    super(key);
      this.type = 'Enum';
      this.component = VueEnumControl;
    this.data = data;
    this.props = { emitter, ikey: key, readonly,
      defaultVal: data['defaultVal'],
      options: data['options']};
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}



var VueEnumUpdateControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal', 'options', 'callback', 'node'],
  template: '<div>\
              <label class="control-label" style="width:20%">{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
              <select class="select-input" type="text" style="width:70%"\
                :readonly="readonly" :value="value" @input="change($event)" \
                @dblclick.stop="" @pointerdown.stop="" @pointermove.stop="">\
                <option v-for="option in options" :value=[option]>{{ option }}<option>\
              </select>\
            </div>',
  data() {
    return {
      value: '',
    }
  },
  methods: {
    change(e){
      this.value = e.target.value;
      this.update();
      this.callback(this.node);
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, this.value)
      // this.emitter.trigger('process');
      }
  },
  mounted() {
    let val = this.getData(this.ikey);
      if (val === undefined) {
        this.value =  this.defaultVal === undefined ? 0: this.defaultVal ;
        this.update()
      }
      else {
        this.value = val
      }
  }
}

class EnumUpdateControl extends Rete.Control {

  constructor(emitter, key, data = {}, callback, node, readonly) {
    super(key);
      this.type = 'EnumUpdate';
      this.component = VueEnumUpdateControl;
    this.data = data;
    this.node = node;
    this.props = { emitter, ikey: key, readonly,
      defaultVal: data['defaultVal'],
      options: data['options'],
      callback:callback,
      node:node
    };
  }

  setValue(val) {
    this.vueContext.value = val;
    this.vueContext.callback(this.node);
  }
}



var VueIntControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal'],
  // replace @input by @blur to trigger event if input lost focus
  template: '<div>\
              <label>{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
              <input class="control-input" type="number" :readonly="readonly" :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
            </div>',
  data() {
    return {
      value: 0,
    }
  },
  methods: {
    change(e){
      this.value = +e.target.value;
      this.update();
      // e.target.previousSibling.innerHTML = this.ikey;
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, this.value)
      // this.emitter.trigger('process');
    }
    },
    mounted() {
      let val = this.getData(this.ikey);
      if (val === undefined) {
        this.value =  this.defaultVal === undefined ? 0: this.defaultVal ;
        this.update()
      }
      else {
        this.value = val
      }
    }
}

class IntControl extends Rete.Control {
  // set defaultVal
  constructor(emitter, key, data = {}, readonly) {
    super(key);
    this.type = 'Float';
    this.component = VueIntControl;
    this.data = data;
    this.props = { emitter, ikey: key, readonly,
      defaultVal: data['defaultVal']};
  }
  setValue(val) {
    console.log("val: ", val);
    this.vueContext.value = val;
  }
}


var VueFloatControl = {
    props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal'],
    // replace @input by @blur to trigger event if input lost focus
    template: '<div>\
                <label>{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
                <input class="control-input" type="number" :readonly="readonly" :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
              </div>',
    data() {
      return {
        value: 0,
      }
    },
    methods: {
      change(e){
        this.value = +e.target.value;
        this.update();
        // e.target.previousSibling.innerHTML = this.ikey;
      },
      update() {
        if (this.ikey)
          this.putData(this.ikey, this.value)
        // this.emitter.trigger('process');
      }
      },
      mounted() {
        let val = this.getData(this.ikey);
        if (val === undefined) {
          this.value =  this.defaultVal === undefined ? 0: this.defaultVal ;
          this.update()
        }
        else {
          this.value = val
        }
      }
  }

class FloatControl extends Rete.Control {
    // set defaultVal
    constructor(emitter, key, data = {}, readonly) {
      super(key);
      this.type = 'Float';
      this.component = VueFloatControl;
      this.data = data;
      this.props = { emitter, ikey: key, readonly,
        defaultVal: data['defaultVal']};
    }
    setValue(val) {
      this.vueContext.value = val;
    }
}


var VueBoolControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal'],
  template: '<div>\
              <label>{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
              <input class="control-input" type="checkbox" :readonly="readonly" :checked="checked" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
            </div>',
  data() {
    return {
      checked: '',
    }
  },
  methods: {
    change(e){
      this.checked = e.target.checked;
      this.update();
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, this.checked)
      // this.emitter.trigger('process');
    }
  },
  mounted() {
    let val = this.getData(this.ikey);
    // console.log("bool, val: ", val);
    // console.log("bool, defaultVal: ", this.defaultVal);
    if (val === undefined) {
      this.checked =  this.defaultVal === undefined ? 0: this.defaultVal ;
      this.update()
    }
    else {
      this.checked = val
    }
  }
}

class BoolControl extends Rete.Control {

  constructor(emitter, key, data={}, readonly) {
    super(key);
      this.type = 'Bool';
      this.component = VueBoolControl;
    this.data = data;
    this.props = { emitter, ikey: key, readonly,
        defaultVal: data['defaultVal']
    };
  }

  setValue(val) {
    this.vueContext.checked = val;
  }
}


var VueColorControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal'],
  template: '<div>\
              <label>{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label\
              input type="color" :readonly="readonly" :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
            </div>',
  data() {
    return {
      value: '',
    }
  },
  methods: {
    change(e){
      this.value = e.target.value;
      this.update();
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, this.value)
      // this.emitter.trigger('process');
    }
  },
  mounted() {
    let val = this.getData(this.ikey);
    if (val === undefined) {
      this.value =  this.defaultVal === undefined ? 0: this.defaultVal ;
      this.update()
    }
    else {
      this.value = val
    }
  }
}

class ColorControl extends Rete.Control {

  constructor(emitter, key, defaultVal, readonly) {
    super(key);
      this.type = 'Color';
      this.component = VueColorControl;
    this.props = { emitter, ikey: key, readonly, defaultVal};
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}


var VueFileControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal'],
  template: '<div style="font-size: 12px" >\
              <label>{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
              <input type="file" :readonly="readonly" :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
            </div>',
  data() {
    return {
      value: '',
      filename: '',
      content: '',
    }
  },
  methods: {
    change(e){
      /* since js shows the fakepath for securety reason
      we need to read the file content, and pushData
      */
      let self = this;
      let file = e.target.files[0];
      let reader = new FileReader();
      this.filename = file.name;
      reader.readAsText(file);
      reader.onload = function() {
        console.log(reader.result);
        self.content = reader.result;
        self.update();
      };
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, {'filename': this.filename, 'content': this.content})
      // this.emitter.trigger('process');
    }
  },
  mounted() {

  }
}

class FileControl extends Rete.Control {

  constructor(emitter, key, defaultVal, readonly) {
    super(key);
      this.type = 'File';
      this.component = VueFileControl;
    this.props = { emitter, ikey: key, readonly, defaultVal};
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}

var VueFloatVectorControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal', 'size'],
  template: '<div>\
              <div><label>{{ikey}}:</label></div> \
              <div>\
              <input class="control-input" style="width: 50px" type="number" v-for="index in size" \
                :readonly="readonly" :value="value[index - 1]" @input="change($event, index)" \
                /> \
              </div>\
            </div>',
  data() {
    return {
      value: [],
    }
  },
  methods: {
    initVector(size, defaultVal) {
      console.log("initVector size: ", size)
      console.log("initVector defaultVal: ", defaultVal)
      var vec = new Array(size);
      if (defaultVal) {
        for(let i = 0; i < size; i++) {
          vec[i] = defaultVal[i];
        }
      }
      else {
        for(let i = 0; i < size; i++) {
          vec[i] = 1;
        }
      }
      return vec;
    },
    change(e, i){
      this.value[i-1] = parseFloat(e.target.value);
      this.update();
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, this.value)
    }
  },
  mounted() {
    let val = this.getData(this.ikey);
    console.log("size: ", this.size)
    console.log("val: ", val)
    if (val === undefined || val.length === 0) {
      let vec = this.initVector(this.size, this.defaultVal);
      console.log("vec: ", vec)
      this.value =  this.defaultVal === undefined ? vec: this.defaultVal ;
      this.update()
    }
    else {
      this.value = val
    }
  }
}

class FloatVectorControl extends Rete.Control {

  constructor(emitter, key, data, readonly) {
    super(key);
    this.type = 'FloatVector';
    this.data = data;
    this.props = { emitter, ikey: key, readonly,
      size: data['size'],
      defaultVal: data['defaultVal']};
    this.component = VueFloatVectorControl;
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}



var VueFloatMatrixControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal', 'size'],
  template: '<div>\
              <label><label>{{ikey}}:</label>\
              <div v-for="index_n in size[0]">\
                <input type="number" v-for="index_m in size[1]" :readonly="readonly" \
                :value="value[(index_n - 1)*size[1] + index_m - 1]" @input="change($event, index_n, index_m)" \
                @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
              </div>\
            </div>',
  data() {
    return {
      value: [],
    }
  },
  methods: {
    initMatrix(size, defaultVal) {
      console.log("initMatrix size: ", size)
      var mat = new Array(size[0]);
      for(let i = 0; i < size[0]; i++) {
          mat[i] = new Array(size[1]);
          if (defaultVal) {
            for(let j = 0; j < size[1]; j++) {
              mat[i][j] = defaultVal[i*size[1] + j];
            }
          }
          else {
            for(let j = 0; j < size[1]; j++) {
              mat[i][j] = 1;
            }
          }
      }
      console.log("matrix: ", mat);
      return mat;
    },
    change(e, i, j){
      this.value[i-1][j-1] = e.target.value;
      this.update();
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, this.value)
    }
  },
  mounted() {
    let val = this.getData(this.ikey);
    if (val === undefined || val.length === 0) {
      let mat = this.initMatrix(this.size, this.defaultVal);
      this.value =  this.defaultVal === undefined ? mat: this.defaultVal ;
      this.update()
    }
    else {
      this.value = val;
    }
  }
}

class FloatMatrixControl extends Rete.Control {

  constructor(emitter, key, data, readonly) {
    super(key);
    this.type = 'FloatMatrix';
    this.data = data;
    this.props = { emitter, ikey: key, readonly,
      size: data['size'],
      defaultVal: data['defaultVal']};
    this.component = VueFloatMatrixControl;
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}



var VuePlotlyBasicChartControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'defaultVal', 'size'],
  template: '<div>\
              <div id="tester" style="width:600px;height:250px;"></div>\
              <label class="control-label">{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
              <input type="text" :readonly="readonly" :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
              <label class="control-label">{{ikey.substring(0,8).padEnd(8, "&nbsp")}}:</label>\
              <input type="text" :readonly="readonly" :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>\
            </div>',
  data() {
    return {
      value: [],
    }
  },
  methods: {

    change(e, i){
      this.value[i-1] = parseFloat(e.target.value);
      this.update();
    },
    update() {
      TESTER = document.getElementById('tester');
      console.log("TESTER: ", TESTER)
	    Plotly.newPlot( TESTER, [{
	    x: [1, 2, 3, 4, 5],
	    y: [1, 2, 4, 8, 16] }], {
	    margin: { t: 0 } } );
    }
  },
  mounted() {
    let val = this.getData(this.ikey);
    this.update();

  }
}

class PlotlyBasicChartControl extends Rete.Control {

  constructor(emitter, key, data, readonly) {
    super(key);
    this.type = 'PlotlyBasicChart';
    this.data = data;
    this.props = { emitter, ikey: key, readonly};
    this.component = VuePlotlyBasicChartControl;
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}



var VueNGLControl = {
  props: ['readonly', 'emitter', 'node', 'ikey', 'getData', 'putData', 'defaultVal'],
  template: '<div>\
                <div id="outer" style="pointer-events: none;"> \
                  <div id="viewport" style="width:300px;height:300px; pointer-events: fill;"></div>\
                </div>\
              <input class="click_button" type="button" @click="update()" value="Update" />\
            </div>',
  data() {
    return {
      value: '',
    }
  },
  methods: {
    change(e){
      this.value = e.target.value;
      this.update();
    },
    update() {
      if (this.ikey){
        this.putData(this.ikey, this.value)
      };
      console.log("this", this)
      // Create NGL Stage object
      var stage = new NGL.Stage( "viewport" );
      // Handle window resizing
      window.addEventListener( "resize", function( event ){
          stage.handleResize();
      }, false );
      if (this.node.inputs.get("Atoms").connections.length > 0) {
        var uuid = this.node.inputs.get("Atoms").connections[0].output.uuid;
        console.log("uuid: ", uuid)
        stage.loadFile("/datas/"+uuid+".cif").then(function (o) {
          o.addRepresentation("licorice")
          o.addRepresentation("spacefill", {
            radiusScale: 0.6
          })
          o.addRepresentation("unitcell")
          stage.autoView()
        })
      }
      // stage.loadFile(this.value, { defaultRepresentation: true } );
    }
  },
  mounted() {
    let val = this.getData(this.ikey);
    if (val === undefined) {
      this.value =  this.defaultVal === undefined ? "": this.defaultVal ;
      this.update()
    }
    else {
      this.value = val
    }
  }
}

class NGLControl extends Rete.Control {

  constructor(emitter, key, node, data={}, readonly) {
    super(key);
    this.type = 'String';
    this.component = VueNGLControl;
    this.data = data;
    console.log("String data: ", this.data)
    console.log("node: ", node)
    this.props = { emitter, ikey: key, node:node, readonly,
      defaultVal: this.data['defaultVal']};
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}

scinode_controls = {
  'Int': IntControl,
  'Float': FloatControl,
  'String': StringControl,
  'Bool': BoolControl,
  'FloatVector': FloatVectorControl,
  'FloatMatrix': FloatMatrixControl,
  'Color': ColorControl,
  'File': FileControl,
  'Enum': EnumControl,
  'PlotlyBasicChart': PlotlyBasicChartControl,
  'NGL': NGLControl,
}

scinode_controls_key = {
  'IntControl': 'Int',
  'FloatControl': 'Float',
  'StringControl': 'String',
  'BoolControl': 'Bool',
  'FloatVectorControl': 'FloatVector',
  'FloatMatrixControl': 'FloatMatrix',
  'ColorControl': 'Color',
  'FileControl': 'File',
  'EnumControl': 'Enum',
  'EnumUpdateControl': 'EnumUpdate',
  'PlotlyBasicChartControl': 'PlotlyBasicChart',
  'NGLControl': 'NGL',
}
