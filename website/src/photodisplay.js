// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";

export default React.createClass({
  onClick() {
    this.props.selectPhoto(null);
  },

  componentDidMount() {
    let rect = this.refs.frame.getBoundingClientRect();
    this.refs.image.setAttribute("src", this.props.photo.getResizedURL(rect.width, rect.height));
  },

  render() {
    return <div className="overlay" onClick={this.onClick}>
      <div ref="frame" className="photoframe">
        <a href={this.props.photo.getDirectURL()}><img ref="image" /></a>
      </div>
    </div>;
  }
});
