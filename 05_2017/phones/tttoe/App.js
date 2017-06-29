import React, { Component } from 'react';
import { Modal, View, StyleSheet, TouchableOpacity, Text, Alert, TextInput, AppRegistry } from 'react-native';


export class ChooseColorModal extends Component {
  state = {
    modalVisible: false,
  }
  
  render() {
    return (
      <Modal
        animationType={"fade"}
        transparent={true}
        visible={this.props.visible}>
        <View style={{backgroundColor:'skyblue'}}>
          <Text> Введите цвет </Text>
          <TextInput onChangeText={this.props._onChangeText} onSubmitEditing={this.props._onOkPressed}/>
        </View>
      </Modal>
    )
  }
}


export class Tyle extends Component {
  render() {
    return (
      <TouchableOpacity onPress={this.props.onPress} onLongPress={this.props.onLongPress}>
        <View style={[styles.tyle, {backgroundColor: this.props.color}]}>
          <Text style={styles.buttonText}> {this.props.symb} </Text>
        </View>
      </TouchableOpacity>  
    )
  }
}

export default class tttoe extends Component {
  constructor(props) {
    super(props);
    this.state = {board: [['', '', ''], ['', '', ''], ['', '', '']], turn_count: 1, tyle_color: '#00D000', tyle_color_modal_visible:false};
  }
  
  setModalVisible(visible) {
    this.setState((prev_state) =>{
      const new_state = prev_state;
      new_state.tyle_color_modal_visible = visible;
      return new_state;
    });
  }
  
  tylePressed(x, y) {
    if (this.state.board[x][y])
      return 0
    this.setState((prev_state) => {
    let symb;
    if (this.state.turn_count % 2) {
        symb = 'X';
     } else {
       symb = '0';
     }
     const new_board = prev_state.board.slice();
     new_board[x][y] = symb;
     let end = this.is_end(new_board);
     if (end) {
       Alert.alert('Game won by ' + end)
     }
     return {board: new_board, turn_count: prev_state.turn_count + 1}
   });
  }
  
  renderTyle(i, j) {
    return (
      <Tyle x={i} y={j} symb={this.state.board[i][j]} onPress={() => this.tylePressed(i, j)} color={this.state.tyle_color} onLongPress={() => this.setModalVisible(!this.state.tyle_color_modal_visible)}/>
      )
  }

  clear_board() {
    this.setState(() => {
      const new_board = [['', '', ''], ['', '', ''], ['', '', '']];
      return {board: new_board, turn_count: 1}
    });
  }
  
  change_tyle_color(color) {
    this.setState((prev_state) => {
      const new_state = prev_state;
      new_state.tyle_color = color;
      return new_state;
    });
  }
  
  check_column(board, x) {
    let column = board[x];
    if (column[0] == column[1] && column[1] == column[2] && column[0] != '') {
      return column[0]
    } else {
      return '';
    }
  }
  
  check_line(board, y) {
    if (board[0][y] == board[1][y] && board[1][y] == board[2][y] && board[0][y] != '') {
      return board[0][y];
    } else {
      return '';
    }
  }
  
  check_diags(board) {
    if (board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[0][0] != '') {
      return board[0][0];
    }
    if (board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[0][2] != '') {
      return board[0][2];
      
    }
    return '';
  }
  
  is_end(board) {
    for (var i = 0; i < 3; i++) {
      if (this.check_line(board, i) != '') return this.check_line(board, i);
      if (this.check_column(board, i) != '') return this.check_column(board, i);
    }
    if (this.check_diags(board) != '') return this.check_diags(board);
  }
  
  __onChangeText(text) {
    this.setState((prev_state) => {
      const new_state = prev_state;
      new_state.tyle_color = text;
      return new_state;
    })
  }
  
  __onOkPressed() {
    this.setState((prev_state) => {
      const new_state = prev_state;
      new_state.tyle_color_modal_visible = false;
      return new_state;
    })
  }
  
  render() {
    return (
        <View style={styles.board}>  
          <View style={{flex:3, flexDirection:'row'}}>
            <View style={styles.column}>
              {this.renderTyle(0, 0)}
              {this.renderTyle(0, 1)}
              {this.renderTyle(0, 2)}
            </View>
            <View style={styles.column}>
              {this.renderTyle(1, 0)}
              {this.renderTyle(1, 1)}
              {this.renderTyle(1, 2)}
            </View>
            <View style={styles.column}>
              {this.renderTyle(2, 0)}
              {this.renderTyle(2, 1)}
              {this.renderTyle(2, 2)}
            </View>
          </View>
          <TouchableOpacity style={{flex: 0.5, backgroundColor: 'skyblue', marginBottom:50}} onPress={() => this.clear_board()}>
            <View style={styles.button}>
              <Text style={styles.buttonText}> RESTART </Text>
            </View>
          </TouchableOpacity> 
          <ChooseColorModal visible={this.state.tyle_color_modal_visible} _onChangeText={(text) => this.__onChangeText(text)} _onOkPressed={() => this.__onOkPressed()}/>
        </View>
    );
  }
}

const styles = StyleSheet.create({
  tyle: {
    backgroundColor: '#00D000',
    height: 100,
    width: 100,
    margin: 10,
    fontSize: 60,
  },
  column: {
    flex:1,
    flexDirection:'column',
    justifyContent:'center',
    alignItems:'center'
  },
  button: {
    flex: 0.5,
    height: 25,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'skyblue',
  },
  board: {
    flex:1,
    backgroundColor: '#065fac'
  },
  buttonText: {
    fontSize: 50,
    padding: 20,
    color: 'white',
    alignText: 'center',
    fontWeight: 'bold',
  },
});

AppRegistry.registerComponent('tttoe', () => SectionListBasics);
