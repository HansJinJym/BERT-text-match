import React from 'react';
// import {EditOutlined, DeleteOutlined} from '@ant-design/icons';
import {Layout, Table, Button, Modal, message } from 'antd';
import InfoDialog from './InfoDialog'
import FeedbackDialog from './FeedbackDialog';
import ApiUtil from '../utils/ApiUtil';
import HttpUtil from '../utils/HttpUtil';

const { Header, Content } = Layout;

const columns = [
    {
        title: '序号',
        dataIndex: 'number',
        width: '10%',
    },
    {
        title: '匹配',
        dataIndex: 'match',
        width: '60%',
    },
    {
        title: '相似度',
        dataIndex: 'similarity',
        width: '30%',
    },
];
const columns1 = columns.slice(0);

function sleep(delay) {
    var start = (new Date()).getTime();
    while ((new Date()).getTime() - start < delay) {
      continue;
    }
}

class HomePage extends React.Component{
    state = {                       // state是当前组件一些可修改的属性，props是传递给子组件的属性（一般只读）
        showInfoDialog: false,      // 显示添加对话框
        showFeedbackDialog: false,
        editingItem: null,          // 对话框编辑的内容
        mData: [],                  // table里的数据
        my_columns: [],             // 列名
    };

    componentDidMount() {
        console.log("in HomePage componentDidMount");
        sleep(100)                  // 调用两次导致线程冲突
        this.getMyColumns();        //获取列名
    }

    getMyColumns(){
        this.setState({
            my_columns: columns1
        })
    }

    showUpdateDialog(item){         // 点击“查询”按钮，调用此函数
        console.log("in showUpdateDialog");
        if(item===undefined){
            item = {};
        }
        console.log(item); //可以通过它来打印查看item
        this.setState({
            showInfoDialog: true,
            editingItem: item, 
        });
    }

    showFeedbackDialog(item){         // 点击“反馈”按钮，调用此函数
        console.log("in showFeedbackDialog");
        this.setState({
            showFeedbackDialog: true,
        });
    }

    handleInfoDialogClose = (ans)=>{
        sleep(4000);
        console.log('接收到数据');
        this.setState({
            showInfoDialog: false,
        });
        this.getData();
    }

    getData(){
        HttpUtil.get(ApiUtil.API_LIST)
            .then(
                stockList =>{
                    this.setState({
                        mData: stockList,
                        showInfoDialog: false,
                    });
                }
            ).catch(error=>{
                message.error(error.message);
            });
    }

    handleFeedbackDialogClose = (ans)=>{
        console.log('反馈数据');
        this.setState({
            showFeedbackDialog: false,
        });
    }

    render(){
        return (
            <Layout>
                <Header>
                    <div style={{lineHeight:'64px', fontSize:"20px", color:"white",textAlign:"center"}}> 
                        文本匹配系统 by 金元明
                    </div>
                </Header>

                <Content >
                    <div style={{ background: '#fff', padding: 24, minHeight: 480 }}>
                        <Button 
                            style={{position:"absolute", right:"70px", top:"20px", // 按钮位置
                            display:this.state.show_back}}                         // 是否显示
                            onClick={()=>this.showUpdateDialog()}                  // 点击触发
                            >                 
                                查询
                        </Button>
                        <Button 
                            style={{position:"absolute", right:"140px", top:"20px", // 按钮位置
                            display:this.state.show_back}}                         // 是否显示
                            onClick={()=>this.showFeedbackDialog()}                  // 点击触发
                            >                 
                                反馈
                        </Button>
                        <Table 
                            columns={this.state.my_columns}
                            dataSource={this.state.mData}           // 从后端数据库获取数据并显示
                            rowKey={item=>item.number}  
                            pagination={{ pageSize: 20 }} 
                            scroll={{ y: 400 }} />

                        <InfoDialog
                            visible={this.state.showInfoDialog}
                            stock={this.state.editingItem}
                            afterClose={()=>{
                                this.setState({showInfoDialog:false});
                            }}
                            onDialogConfirm={this.handleInfoDialogClose} />

                        <FeedbackDialog
                            visible={this.state.showFeedbackDialog}
                            // stock={this.state.editingItem}
                            afterClose={()=>{
                                this.setState({showFeedbackDialog:false});
                            }}
                            onDialogConfirm={this.handleFeedbackDialogClose} />

                    </div>
                </Content>
            </Layout>
        );
    }
}

export default HomePage;