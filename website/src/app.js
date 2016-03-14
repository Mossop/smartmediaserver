// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";
import ReactDOM from "react-dom";

import injectTapEventPlugin from 'react-tap-event-plugin';

// Needed for onTouchTap
// Can go away when react 1.0 release
// Check this repo:
// https://github.com/zilverline/react-tap-event-plugin
injectTapEventPlugin();

import AppBar from 'material-ui/lib/app-bar';

import FolderNav from "./foldernav";
import FolderView from "./folderview";
import PhotoDisplay from "./photodisplay";

async function fetchJSON(url) {
  let response = await fetch(url);
  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return await response.json();
}

function makeHierarchy(model, name) {
  return {
    root: {
      pk: null,
      model: `website.${model}`,
      fields: {
        name,
      }
    },
    folders: new Map()
  };
}

const AppState = {
  data: {
    hierarchies: [
      makeHierarchy("physicalfolder", "All Photos"),
      makeHierarchy("virtualfolder", "Virtual Folders"),
    ],
    photos: new Map()
  },

  getHierarchy(folder) {
    for (let hierarchy of this.data.hierarchies) {
      if (hierarchy.root.model == folder.model) {
        return hierarchy;
      }
    }
    return null;
  },

  async fetchFolderPhotos(folder) {
    if (!folder.pk) {
      return;
    }

    try {
      let model = folder.model.substring(8);
      let json = await fetchJSON(`/${model}/${folder.pk}/photos`);

      let photos = [];
      for (let photo of json) {
        if (!this.data.photos.has(photo.pk)) {
          this.data.photos.set(photo.pk, photo);
        }
        photos.push(photo.pk);
      }

      folder.photos = photos;
      renderApp();
    } catch (e) {
      console.error(e);
    }
  },

  async fetchHierarchy(hierarchy) {
    try {
      let model = hierarchy.root.model.substring(8);
      let json = await fetchJSON(`/${model}/list`);
      let folders = new Map();
      for (let photo of json) {
        folders.set(photo.pk, photo);
      }

      hierarchy.folders = folders;
      renderApp();
    } catch (e) {
      console.error(e);
    }
  },
};

const App = React.createClass({
  getInitialState() {
    return {
      navOpen: false,
      selectedHierarchy: AppState.data.hierarchies[0],
      selectedFolder: AppState.data.hierarchies[0].root,
      selectedPhoto: null,
    };
  },

  componentDidMount() {
    for (let hierarchy of this.props.hierarchies) {
      AppState.fetchHierarchy(hierarchy);
    }
  },

  toggleNav() {
    this.setState({ navOpen: !this.state.navOpen });
  },

  selectFolder(folder) {
    this.setState({
      navOpen: false,
      selectedHierarchy: AppState.getHierarchy(folder),
      selectedFolder: folder,
      selectedPhoto: null
    });

    if (!folder.photos) {
      AppState.fetchFolderPhotos(folder);
    }
  },

  selectPhoto(photo) {
    this.setState({ selectedPhoto: photo });
  },

  render() {
    let photoView = "";
    if (this.state.selectedPhoto) {
      photoView = <PhotoDisplay folder={this.state.selectedFolder} photo={this.state.selectedPhoto} selectPhoto={this.selectPhoto}/>;
    }
    return <div id="appcontent">
      <AppBar title={this.state.selectedFolder.fields.name} onLeftIconButtonTouchTap={this.toggleNav} />
      <FolderNav {...this.props} open={this.state.navOpen} toggleNav={this.toggleNav} selectFolder={this.selectFolder} />
      <div id="maincontent">
        <FolderView {...this.props} folder={this.state.selectedFolder} hierarchy={this.state.selectedHierarchy} selectFolder={this.selectFolder} selectPhoto={this.selectPhoto} />
        {photoView}
      </div>
    </div>;
  }
});

function renderApp() {
  ReactDOM.render(<App {...AppState.data}/>, document.getElementById("app"));
}

renderApp();
