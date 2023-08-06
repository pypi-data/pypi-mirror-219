

async function refreshNodetreeNode() {
    // reload table
    $('#data').DataTable().ajax.reload();
};

$(document).ready(function () {
    if (nodetree_data['uuid'] != '') {
        $('#data').DataTable({
            ajax: '/nodetrees/api/'+nodetree_data['uuid'] +'/nodes',
            serverSide: true,
            columns: [
                {data: null , "render": function (data,type,row) { return '<a class="btn btn-primary" href="/nodes/' + row.uuid +'" role="button">View</a>' }},
                {data: 'index'},
                {data: 'inner_id'},
                {data: 'name'},
                {data: 'state'},
                {data: 'action'},
                // {data: null , "render": function (data,type,row) { return '<a class="btn btn-primary" onclick="actionNode(\'' + row.uuid + '\')" role="button">Reset</a>'}},
                {data: null , "render": function (data,type,row) { return '<a class="btn btn-primary" onclick="actionNode(\'' + row.uuid + '\', \'PAUSE\')" role="button">Pause</a>'}},
                {data: null , "render": function (data,type,row) { return '<a class="btn btn-primary" onclick="actionNode(\'' + row.uuid + '\', \'PLAY\')" role="button">Play</a>'}},
                // {data: null , "render": function (data,type,row) { return '<a class="btn btn-primary" onclick="actionNode(\'' + row.uuid + '\')" role="button">Delete</a>'}}
            //   {data: 'action', orderable: false},
            ],
        });
    }
    document.getElementById("description-pre").textContent = JSON.stringify(nodetree_data, undefined, 2)
});
