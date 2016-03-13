// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";
import ReactDOM from "react-dom";

import CircularProgress from "material-ui/lib/circular-progress";

import FolderList from "./folderlist";
import ContentArea from "./contentarea";

async function fetchJSON(url) {
  let response = await fetch(url);
  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return await response.json();
}

const App = React.createClass({
  getInitialState() {
    return {
      physicalFolders: null,
      virtualFolders: null,
      photos: null,
      selectedFolder: null,
      selectedPhoto: null,
    };
  },

  componentDidMount() {
    fetchJSON("/physicalfolder/list").then(data => {
      this.setState({ physicalFolders: data });
    }, console.error);

    fetchJSON("/virtualfolder/list").then(data => {
      this.setState({ virtualFolders: data });
    }, console.error);
  },

  selectFolder(folder) {
    console.log("select", folder);
    this.setState({ selectedFolder: folder, selectedPhoto: null });

    if (!folder.photos) {
      let model = folder.model.substring(8);
      fetchJSON(`/${model}/${folder.pk}/photos`).then(photos => {
        folder.photos = photos;
        this.setState({ selectedFolder: folder });
      }, console.error);
    }
  },

  selectPhoto(photo) {
    this.setState({ selectedPhoto: photo });
  },

  render() {
    if ((this.state.physicalFolders == null) || (this.state.virtualFolders == null)) {
      return <div id="appcontent">
        <div className="flex-center">
          <CircularProgress size={2} />
        </div>
      </div>;
    }

    return <div id="appcontent">
      <FolderList {...this.state} onSelectFolder={this.selectFolder}/>
      <ContentArea {...this.state} onSelectPhoto={this.selectPhoto}/>
    </div>;
  }
});

ReactDOM.render(
  <App/>,
  document.getElementById("app")
);
