// This file is part of Invenio-DAMAP
// Copyright (C) 2023-2024 Graz University of Technology.
// Copyright (C) 2023-2024 TU Wien.
//
// Invenio-DAMAP is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import { Button, Icon } from "semantic-ui-react";

import PropTypes from "prop-types";

// TODO: Make overridable
export class DMPAuthButton extends React.Component {
  render() {
    const { loading, checkRemoteAccountAvailable } = this.props;
    return (
      <Button
        fluid
        onClick={checkRemoteAccountAvailable}
        disabled={false}
        primary
        size="medium"
        aria-haspopup="dialog"
        icon
        labelPosition="left"
        loading={loading}
      >
        <Icon name="plus square" />
        {"Authenticate with DAMAP"}
      </Button>
    );
  }
}

DMPAuthButton.propTypes = {
  loading: PropTypes.bool.isRequired,
  checkRemoteAccountAvailable: PropTypes.func.isRequired,
};
