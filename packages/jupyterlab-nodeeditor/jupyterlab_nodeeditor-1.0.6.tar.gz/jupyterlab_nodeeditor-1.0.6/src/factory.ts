import { NodeEditorDocumentWidget, NodeEditorWidget } from "./widget"
import { NodeBookModel } from "./model";
import { ABCWidgetFactory, DocumentRegistry } from '@jupyterlab/docregistry';
import {
    JupyterFrontEnd
} from "@jupyterlab/application"
import {
    ICommandPalette
} from "@jupyterlab/apputils";
import { ISettingRegistry } from '@jupyterlab/settingregistry';
export class NodeEditorDocumentWidgetFactory
    extends ABCWidgetFactory<NodeEditorDocumentWidget, NodeBookModel>{
    app: JupyterFrontEnd
    palette: ICommandPalette
    settings: ISettingRegistry
    constructor(
        option: DocumentRegistry.IWidgetFactoryOptions,
        app: JupyterFrontEnd,
        palette: ICommandPalette,
        settings: ISettingRegistry,
    ) {
        super(option);
        this.app = app
        this.palette = palette
        this.settings = settings
    }

    protected createNewWidget(
        context: DocumentRegistry.IContext<NodeBookModel>,
        source?: NodeEditorDocumentWidget | undefined):
        NodeEditorDocumentWidget {
        return new NodeEditorDocumentWidget({
            context,
            content: new NodeEditorWidget(
                context,
                this.app,
                this.palette,
                this.settings
            )
        })
    }
}

