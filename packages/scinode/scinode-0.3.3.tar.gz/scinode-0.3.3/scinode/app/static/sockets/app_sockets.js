var SocketGeneral = new Rete.Socket('SocketGeneral');

var SocketFloat = new Rete.Socket('SocketFloat');
SocketFloat.combineWith(SocketGeneral);
var SocketInt = new Rete.Socket('SocketInt');
SocketInt.combineWith(SocketGeneral);
var SocketString = new Rete.Socket('SocketString');
SocketString.combineWith(SocketGeneral);
var SocketBool = new Rete.Socket('SocketBool');
SocketBool.combineWith(SocketGeneral);

var SocketEnum = new Rete.Socket('SocketEnum');
SocketEnum.combineWith(SocketGeneral);
var SocketFloatVector = new Rete.Socket('SocketFloatVector');
SocketFloatVector.combineWith(SocketGeneral);
var SocketFloatMatrix = new Rete.Socket('SocketFloatMatrix');
SocketFloatMatrix.combineWith(SocketGeneral);


// SocketGeneral
SocketGeneral.combineWith(SocketFloat);
SocketGeneral.combineWith(SocketInt);
SocketGeneral.combineWith(SocketString);
SocketGeneral.combineWith(SocketBool);
SocketGeneral.combineWith(SocketEnum);
SocketGeneral.combineWith(SocketFloatVector);
SocketGeneral.combineWith(SocketFloatMatrix);

scinode_sockets = {
    'General': SocketGeneral,
    'Int': SocketInt,
    'Float': SocketFloat,
    'String': SocketString,
    'Bool': SocketBool,
    'Enum': SocketEnum,
    'FloatVector': SocketFloatVector,
    'FloatMatrix': SocketFloatMatrix,
  }
