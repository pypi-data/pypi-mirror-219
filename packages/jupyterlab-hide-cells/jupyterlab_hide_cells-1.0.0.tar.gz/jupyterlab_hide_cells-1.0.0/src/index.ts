import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from "@jupyterlab/application";
import { IMainMenu } from "@jupyterlab/mainmenu";
import { Menu } from "@lumino/widgets";
import {
  PLUGIN_ID,
  METADATA_KEY_HIDDEN_CELL_ENABLED,
  HIDDENCELL_ENABLED_CLASS,
} from "./config";
import {
  INotebookTools,
  NotebookPanel,
  Notebook,
  INotebookTracker,
} from "@jupyterlab/notebook";
import { Cell } from "@jupyterlab/cells";

let VIEWALLCELLS = false;

const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [IMainMenu, INotebookTracker, INotebookTools],
  activate: activate,
};

async function activate(
  app: JupyterFrontEnd,
  mainMenu: IMainMenu,
  notebookTracker: INotebookTracker,
  notebookTools: INotebookTools,
) {
  console.log(`${PLUGIN_ID} activated!`);

  //create a new command
  const command1: string = `${PLUGIN_ID}:hide_cell`;
  app.commands.addCommand(command1, {
    label: () => {
      let selectedCells = notebookTools.selectedCells;
      if (selectedCells.length == 0) {
        throw Error(
          `[${PLUGIN_ID}]: Could not find any currently selected cell!`,
        );
      }
      let checkboxCells = selectedCells.filter((cell: Cell) => {
        return (
          cell.model.metadata.get(METADATA_KEY_HIDDEN_CELL_ENABLED) || false
        );
      });
      if (checkboxCells.length > 0) return "Show this cell";
      return "Hide this cell";
    },
    execute: () => {
      let selectedCells = notebookTools.selectedCells;
      if (selectedCells.length == 0) {
        throw Error(
          `[${PLUGIN_ID}]: Could not find any currently selected cell!`,
        );
      }
      hideCellMetadata(notebookTracker.activeCell as Cell);
    },
  });

  console.log(app.commands);

  app.contextMenu.addItem({
    command: PLUGIN_ID + ":hide_cell",
    selector: ".jp-Cell",
    rank: 0,
  });

  // Create a new view menu
  let viewMenu = mainMenu.viewMenu;
  const { commands } = app;
  commands.addCommand("${PLUGIN_ID}:view_all_cells", {
    execute: () => {
      VIEWALLCELLS = !VIEWALLCELLS;
      notebookTracker.forEach((nbPanel) => {
        nbPanel.content.widgets.forEach((cell) => {
          hideCell(cell);
        });
      });
    },
    isToggled: () => VIEWALLCELLS,
    label: "View All Cells (incl. Hidden Cells)",
  });
  let viewMenuOption: Menu.IItemOptions = {
    command: "${PLUGIN_ID}:view_all_cells",
  };
  viewMenu.addGroup([viewMenuOption]);

  //check if metadata ob an active cell has been changed
  notebookTracker.activeCellChanged.connect(() => {
    const currentCell = notebookTracker.activeCell as Cell;
    currentCell.model.metadata.changed.connect(() => {
      hideCell(currentCell);
    });
  });

  //each time a new notebook is in focus show / hide cells corresponding to VIEWALLCELLS
  notebookTracker.currentChanged.connect(() => {
    const notebookPanel = notebookTracker.currentWidget as NotebookPanel;
    const notebook = notebookPanel.content as Notebook;
    if (notebook.model) {
      notebook.model.stateChanged.connect(async () => {
        hideAllCellsOfNotebook(notebook);
      });
    }
  });
}

const hideAllCellsOfNotebook = (notebook: Notebook) => {
  notebook.widgets.forEach((cell) => {
    hideCell(cell);
  });
};

const hideCell = (cell: Cell) => {
  if (VIEWALLCELLS) {
    //show all cells
    let metatdata =
      cell.model.metadata.get(METADATA_KEY_HIDDEN_CELL_ENABLED) || false;
    if (metatdata == true) {
      cell.addClass(HIDDENCELL_ENABLED_CLASS);
    } else {
      cell.removeClass(HIDDENCELL_ENABLED_CLASS);
    }
    cell.show();
  } else {
    //hide all cells with corresponding tag
    let metatdata =
      cell.model.metadata.get(METADATA_KEY_HIDDEN_CELL_ENABLED) || false;
    if (metatdata == true) {
      cell.removeClass(HIDDENCELL_ENABLED_CLASS);
      cell.hide();
    }
  }
};

const hideCellMetadata = (cell: Cell) => {
  const metadata = cell.model.metadata;
  if (!!metadata.get(METADATA_KEY_HIDDEN_CELL_ENABLED)) {
    cell.model.metadata.set(METADATA_KEY_HIDDEN_CELL_ENABLED, false);
    cell.removeClass(HIDDENCELL_ENABLED_CLASS);
    return;
  }
  cell.model.metadata.set(METADATA_KEY_HIDDEN_CELL_ENABLED, true);
  cell.addClass(HIDDENCELL_ENABLED_CLASS);
};

// noinspection JSUnusedGlobalSymbols
export default plugin;
