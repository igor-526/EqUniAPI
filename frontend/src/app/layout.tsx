import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import React from "react";
import {ConfigProvider} from "antd";
import ru_RU from 'antd/lib/locale/ru_RU';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Equestrian App',
    description: 'Horse management application',
};

export default function RootLayout({
                                       children,
                                   }: {
    children: React.ReactNode;
}) {
    return (
        <ConfigProvider locale={ru_RU}>
            <html lang="ru">
                <body className={inter.className}>
                    {children}
                </body>
            </html>
        </ConfigProvider>

    );
}