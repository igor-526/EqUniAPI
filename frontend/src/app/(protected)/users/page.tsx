"use client"

import { useEffect, useState } from 'react';
import TablePagination from "@/ui/pagination";
import TableWithFilters from "@/ui/tableWithFilters";
import { UserListRequestParamsType, UserGroupMetadataOutDtoType, UserPageMetadataType, UserTableDataItemType, UserOutDtoType } from '@/types/api/users';
import { getUsersTableColumns } from './usersTableColumns';
import { getUsersList, getUsersPageMetadata } from '@/api/users';
import { Button } from 'antd';
import UserRegistrationModal from './userRegistrationModal';

const UsersPage: React.FC = () => {
    const [filters, setFilters] = useState<UserListRequestParamsType>({
        limit: 10,
        offset: 0,
        name: undefined,
        username: undefined,
        email: undefined,
        groups: [],
        sort: []
    });
    const [loading, setLoading] = useState<boolean>(false);
    const [usersData, setUsersData] = useState<UserTableDataItemType[]>([]);
    const [usersDataCount, setUsersDataCount] = useState<number>(0);
    const [pageMetadata, setPageMetadata] = useState<UserPageMetadataType>({
        user_groups: [],
    });

    const [registrationModalOpen, setRegistrationModalOpen] = useState<boolean>(false);

    const usersTableColumns = getUsersTableColumns(filters, setFilters, pageMetadata);

    const onClickRegistrationButtonListener = () => {
        setRegistrationModalOpen(true)
    }

    const refreshUsersList = () => {
        setFilters((prevFilters) => ({
            ...prevFilters
        }));
    };

    const headerElements = <>
        <div className="flex items-end">
            <TablePagination
                setFilters={setFilters}
                total={usersDataCount}
            />
            <Button onClick={onClickRegistrationButtonListener}>Регистрация</Button>
        </div>
    </>

    useEffect(() => {
        getUsersPageMetadata().then(data => {
            setPageMetadata({
                user_groups: data.data.user_groups.map((item: UserGroupMetadataOutDtoType) => ({
                    label: item.title,
                    value: item.id,
                    key: item.id.toString()
                }))
            })
        })

    }, [])
    useEffect(() => {
        setLoading(true);
        getUsersList(filters).then(data => {
            setUsersDataCount(data.data.count)
            setUsersData(
                data.data.items.map(
                    (item: UserOutDtoType) => ({
                        ...item,
                        key: item.id.toString(),
                    })
                )
            );
            setLoading(false)
        })
    }, [filters]);

    return (
        <>
            <TableWithFilters
                tableColumns={usersTableColumns}
                tableData={usersData}
                tableLoading={loading}
                filtersElements={headerElements}
            // onRowListener={onRowListener}
            />
            <UserRegistrationModal
            registrationModalOpen={registrationModalOpen}
            setRegistrationModalOpen={setRegistrationModalOpen}
            onRegistered={refreshUsersList}
            />
        </>
    )
}

export default UsersPage;
