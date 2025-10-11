import { useState } from 'react';
import {MenuFoldOutlined, MenuUnfoldOutlined} from '@ant-design/icons';
import { Button, Layout, Menu } from 'antd';
import {Outlet, useNavigate} from "react-router";
import {useAppSelector} from "./hooks/redux";

const { Header, Sider, Content } = Layout;

const BaseLayout = () => {
    const [collapsed, setCollapsed] = useState(true)
    const navigate = useNavigate()
    const items = [
        {
            key: 'main',
            label: 'Дэшборд',
            onClick: () => {navigate('/')}
        },
        {
            key: 'horses',
            label: 'Лошади',
            onClick: () => {navigate('/horses')}
        },
        {
            key: 'logout',
            label: 'Выйти',
            onClick: () => {navigate('/login')}
        },
    ]
    const pageTitle = useAppSelector(state => state.layout.pageTitle)

    return (
        <Layout className="h-screen">
            <Sider
                collapsedWidth="50"
                trigger={null}
                collapsible
                collapsed={collapsed}
            >
                <Menu
                    theme="dark"
                    mode="vertical"
                    defaultSelectedKeys={['1']}
                    items={items}
                />
            </Sider>
            <Layout className="flex flex-col h-screen overflow-y-hidden">
                <Header style={{ padding: 0, background: "#FFFFFF" }}>
                    <Button
                        type="text"
                        icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
                        onClick={() => setCollapsed(!collapsed)}
                        style={{
                            fontSize: '16px',
                            width: 64,
                            height: 64,
                        }}
                    />
                    <span style={{color: "grey", fontSize: 18, fontWeight: 600}}>{pageTitle}</span>
                </Header>
                <Content
                    style={{
                        margin: '24px 16px',
                        padding: 24,
                        minHeight: 280,
                        background: "#FFFFFF",
                        borderRadius: 8,
                    }}
                >
                    <div className="h-full overflow-y-auto overflow-x-auto">
                        <Outlet />
                    </div>
                </Content>
            </Layout>
        </Layout>
    );
};

export default BaseLayout;