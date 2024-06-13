def style():
    return  """
                QPushButton {
                    background-color: #049fb5;
                    border: none;
                    color: white;
                    padding: 8px 12px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 16px;
                    margin: 4px 2px;
                    border-radius: 4px;
                }

                QPushButton:hover {
                    background-color: #01709f;
                }

                QComboBox {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px 15px 2px 5px;
                    min-width: 75px;
                }

                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 20px;
                    border-left-width: 1px;
                    border-left-color: darkgray;
                    border-left-style: solid;
                }
            """