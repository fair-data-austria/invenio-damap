// This file is part of Invenio-DAMAP
// Copyright (C) 2023-2024 Graz University of Technology.
// Copyright (C) 2023-2024 TU Wien.
//
// Invenio-DAMAP is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.


import React from "react";
import { Button, Icon } from "semantic-ui-react";
import { http } from "react-invenio-forms";

import PropTypes from "prop-types";

import { DMPModal } from "./DMPModal";
import { DMPAuthButton } from "./DMPAuthButton";


export class DMPButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      record: props.record,
      disabled: props.disabled,
      open: props.open,
      linkedAccount: null,
      loading: false,
    };
  }

  checkRemoteAccountAvailable = async () => {
    this.setState({ loading: true, linkedAccount: null });

    try {
      let linkedAccount = await http.get("/api/invenio_damap/damap/dmp");
      this.setState({ linkedAccount: linkedAccount });
    } catch (e) {}
    this.setState({ loading: false });
  };

  handleOpen = () => {
    this.setState({
      open: true,
    });
  };

  handleClose = () => {
    this.setState({
      open: false,
    });
  };

  componentDidMount() {
    this.checkRemoteAccountAvailable();
  }

  render() {
    const { disabled, open, record, linkedAccount, loading } = this.state;

    const remoteAccountAvailable = linkedAccount != null;

    return (
      <>
        {!remoteAccountAvailable && (
          <DMPAuthButton
            loading={loading}
            checkRemoteAccountAvailable={this.checkRemoteAccountAvailable}
          ></DMPAuthButton>
        )}
        {remoteAccountAvailable && (
          <>
            <Button
              fluid
              onClick={this.handleOpen}
              disabled={disabled}
              primary
              size="medium"
              aria-haspopup="dialog"
              icon
              labelPosition="left"
            >
              <Icon name="plus square" />
              {"Add to DMP"}
            </Button>
            {open && (
              <DMPModal
                open={open}
                handleClose={this.handleClose}
                record={record}
              />
            )}
          </>
        )}
      </>
    );
  }
}

DMPButton.propTypes = {
  disabled: PropTypes.bool,
  record: PropTypes.object.isRequired,
  open: PropTypes.bool,
};

DMPButton.defaultProps = {
  disabled: false,
  open: false,
};
