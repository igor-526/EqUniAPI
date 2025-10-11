import {useState} from 'react';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import {Alert, Button, Form, Input} from 'antd';
import {useNavigate} from "react-router";
import authApiLogin from "../axios/authApi.ts";


const LoginPage = () => {
    const [showError, setShowError] = useState(false);
    const navigate = useNavigate()

    const onFinish = (values: any) => {
        authApiLogin(values.username, values.password).then(response => {
            localStorage.setItem('accessToken', response.access);
            navigate('/dashboard');
        }).catch(error => {
            if (error.response.status === 401) {
                setShowError(true);
            }
        })
    };

    return (
        <div className="w-screen h-screen flex justify-center items-center">
            <div className="p-5 shadow-lg">
                <Form
                    name="login"
                    initialValues={{ remember: true }}
                    onFinish={onFinish}
                >
                    <Form.Item
                        name="username"
                        rules={[{ required: true, message: 'Введите логин' }]}
                    >
                        <Input prefix={<UserOutlined />} placeholder="Логин" />
                    </Form.Item>
                    <Form.Item
                        name="password"
                        rules={[{ required: true, message: 'Введите пароль' }]}
                    >
                        <Input prefix={<LockOutlined />} type="password" placeholder="Пароль" />
                    </Form.Item>
                    <Form.Item>
                        <Button block type="primary" htmlType="submit">
                            Войти
                        </Button>
                    </Form.Item>
                </Form>
                {showError && <Alert message="Неверный логин или пароль" type="error" />}
            </div>
        </div>


    );
};
export default LoginPage;