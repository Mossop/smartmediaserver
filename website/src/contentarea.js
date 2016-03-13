// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";

import CircularProgress from "material-ui/lib/circular-progress";
import Paper from "material-ui/lib/paper";

const Thumbnail = React.createClass({
  onClick() {
    this.props.selectPhoto(this.props.photo);
  },

  render() {
    let src = `/photo/${this.props.photo.pk}/thumbnail/150`;
    return <Paper zDepth={2}>
      <div className="thumbnail">
        <img onClick={this.onClick} src={src} />
      </div>
    </Paper>;
  }
});

const Photo = React.createClass({
  render() {
    let src = `/photo/${this.props.photo.pk}/download`;
    return <img src={src}/>
  }
});

export default React.createClass({
  render() {
    if (this.props.selectedPhoto) {
      return <div className="contentarea photo">
        <Photo photo={this.props.selectedPhoto}/>
      </div>;
    } else if (this.props.selectedFolder) {
      if (!this.props.selectedFolder.photos) {
        return <div className="contentarea loading">
          <div className="flex-center">
            <CircularProgress size={2} />
          </div>
        </div>;
      }

      return <div className="contentarea folder">
        <div className="grid">
          {this.props.selectedFolder.photos.map(p => <Thumbnail key={p.pk} selectPhoto={this.props.onSelectPhoto} photo={p}/>)}
        </div>
      </div>;
    }

    return <div className="contentarea"></div>;
  }
});
