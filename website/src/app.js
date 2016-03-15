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

import smartmedia from "./smartmedia";

import AppBar from 'material-ui/lib/app-bar';

import FolderNav from "./foldernav";
import FolderView from "./folderview";
import PhotoDisplay from "./photodisplay";

const AppState = {
  roots: []
};

const App = React.createClass({
  getInitialState() {
    return {
      navOpen: false,
      selectedFolder: null,
      selectedPhoto: null,
    };
  },

  toggleNav() {
    this.setState({ navOpen: !this.state.navOpen });
  },

  selectFolder(folder) {
    console.log("Select folder", folder.id, folder.name);
    this.setState({
      navOpen: false,
      selectedFolder: folder,
      selectedPhoto: null
    });

    renderAfter(folder.loadContents());
  },

  selectPhoto(photo) {
    this.setState({ selectedPhoto: photo });
  },

  render() {
    let photoView = "";
    if (this.state.selectedPhoto) {
      photoView = <PhotoDisplay folder={this.state.selectedFolder} photo={this.state.selectedPhoto} selectPhoto={this.selectPhoto}/>;
    }
    let name = this.state.selectedFolder ? this.state.selectedFolder.name : "Smart Media";
    return <div id="appcontent">
      <AppBar title={name} onLeftIconButtonTouchTap={this.toggleNav} />
      <FolderNav {...this.props} open={this.state.navOpen} toggleNav={this.toggleNav} selectFolder={this.selectFolder} />
      <div id="maincontent">
        <FolderView {...this.props} folder={this.state.selectedFolder} selectFolder={this.selectFolder} selectPhoto={this.selectPhoto} />
        {photoView}
      </div>
    </div>;
  }
});

async function renderAfter(promise) {
  try {
    await promise;
    ReactDOM.render(<App {...AppState}/>, document.getElementById("app"));
  } catch (e) {
    console.error(e);
  }
}

renderAfter(smartmedia.loadRoots().then(r => AppState.roots = r));
