import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILayoutRestorer,
} from '@jupyterlab/application';
import {
  WidgetTracker,
  IWidgetTracker,
  ICommandPalette,
} from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { Token } from '@lumino/coreutils';
import { NodeEditorDocumentWidgetFactory } from './factory';
import { NodeEditorDocumentWidget } from "./widget"

const FACTORY = 'node-editor';
const PLUGIN_ID = 'jupyterlab_nodeeditor:plugin'
export const INodeEditorDocTracker =
  new Token<IWidgetTracker<NodeEditorDocumentWidget>>("NodeEditorDocumentWidget")

/**
 * Initialization data for the jupyterlab_nodeeditor extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [ILayoutRestorer, ICommandPalette, ISettingRegistry],
  provides: INodeEditorDocTracker,
  activate: (
    app: JupyterFrontEnd,
    restorer: ILayoutRestorer,
    palette: ICommandPalette,
    settings: ISettingRegistry
  ) => {
    console.log('节点编辑器激活');
    const namespace = "node-editor-doc"
    const tracker = new WidgetTracker<NodeEditorDocumentWidget>({ namespace });

    // Handle state restoration.
    if (restorer) {
      // When restoring the app, if the document was open, reopen it
      restorer.restore(tracker, {
        command: 'docmanager:open',
        args: (widget) => ({ path: widget.context.path, factory: FACTORY }),
        name: (widget) => widget.context.path,
      });
    }

    // 将 widget factory注册到 document manager 
    const widgetFactory = new NodeEditorDocumentWidgetFactory({
      name: FACTORY,
      modelName: 'notebook',
      fileTypes: ["notebook"],
      defaultFor: ["notebook"],
      canStartKernel: true,
      preferKernel: true
    }, app, palette, settings);

    // 当widget创建时，将其加入到tracker里
    widgetFactory.widgetCreated.connect((sender, widget) => {
      // 通知tracker的实例是否需要保存需要的数据
      widget.context.pathChanged.connect(() => {
        tracker.save(widget)
      })
      tracker.add(widget)
    })

    // 注册 widget factory
    app.docRegistry.addWidgetFactory(widgetFactory)
  }
};

export default plugin;
