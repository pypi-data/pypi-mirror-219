var container = document.querySelector('#rete');
// var editor = new Rete.NodeEditor('scinode@0.3.2', container);
var editor = new ScinodeEditor('scinode@0.3.2', container);
editor.use(ConnectionPlugin.default);
editor.use(VueRenderPlugin.default);
editor.use(ContextMenuPlugin.default, {
    delay: 0,
    allocate(component) {
        return [component.catalog]
    },
    rename(component) {
        return component.name;
    },
});
editor.use(AreaPlugin);
editor.use(HistoryPlugin);
editor.use(ConnectionMasteryPlugin.default);
editor.use(MinimapPlugin.default);
editor.use(CommentPlugin.default, {
    margin: 20 // indent for new frame comments by default 30 (px)
})
// editor.use(MinimapPlugin);
var engine = new Rete.Engine('scinode@0.3.2');
editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async () => {
    console.log('process');
    await engine.abort();
    // await engine.process(editor.toJSON());
});
