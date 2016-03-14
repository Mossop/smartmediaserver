// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";

export default React.createClass({
  onClick() {
    this.props.selectPhoto(null);
  },

  render() {
    return <div className="overlay" onClick={this.onClick}>
      <div className="photoframe">
        <img src={`/photo/${this.props.photo.pk}/download`}/>
      </div>
    </div>;
  }
});
