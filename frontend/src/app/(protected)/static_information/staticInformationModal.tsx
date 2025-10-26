import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Button, Input, Modal, Radio, message } from 'antd';
import { GetStaticInformationModalElementType } from '@/types/ui/staticInformationModal';
import type { StaticInformationAvailableAsType } from '@/types/api/static_information';
import type { RadioChangeEvent } from 'antd/es/radio';
import {
    createStatisticInformation,
    deleteStatisticInformation,
    updateStatisticInformation,
} from '@/api/static_information';

const StaticInformationModal: GetStaticInformationModalElementType = ({
    staticInformationModalOpen,
    setStaticInformationModalOpen,
    selectedStaticInformation,
    onAction
}) => {
    const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
    const [infoTitle, setInfoTitle] = useState<string>("");
    const [infoName, setInfoName] = useState<string>("");
    const [infoAsType, setInfoAsType] = useState<StaticInformationAvailableAsType>("string");
    const [infoValue, setInfoValue] = useState<string>("");
    const [deleteConfirmVisible, setDeleteConfirmVisible] = useState<boolean>(false);
    const [deleteLoading, setDeleteLoading] = useState<boolean>(false);

    const isEditMode = useMemo(
        () => Boolean(selectedStaticInformation),
        [selectedStaticInformation]
    );

    const typeOptions: { label: string; value: StaticInformationAvailableAsType }[] = useMemo(
        () => [
            { label: "string", value: "string" },
            { label: "number", value: "number" },
            { label: "float", value: "float" },
            { label: "boolean", value: "boolean" },
            { label: "json", value: "json" },
            { label: "date", value: "date" },
            { label: "time", value: "time" },
            { label: "datetime", value: "datetime" },
        ],
        []
    );

    const resetForm = useCallback(() => {
        setInfoTitle("");
        setInfoName("");
        setInfoAsType("string");
        setInfoValue("");
        setConfirmLoading(false);
        setDeleteConfirmVisible(false);
        setDeleteLoading(false);
    }, []);

    useEffect(() => {
        if (!staticInformationModalOpen) {
            setConfirmLoading(false);
            return;
        }

        if (selectedStaticInformation) {
            setInfoTitle(selectedStaticInformation.title);
            setInfoName(selectedStaticInformation.name);
            setInfoAsType(selectedStaticInformation.as_type);
            setInfoValue(selectedStaticInformation.value ?? "");
        } else {
            resetForm();
        }
    }, [staticInformationModalOpen, selectedStaticInformation, resetForm]);

    useEffect(() => {
        if (infoAsType === "boolean" && infoValue !== "true" && infoValue !== "false") {
            setInfoValue("true");
        }
    }, [infoAsType, infoValue]);

    const handleErrorResponse = (error: any) => {
        const errorData = error?.response?.data;
        if (typeof errorData === "string") {
            message.error(errorData);
            return;
        }
        if (errorData && typeof errorData === "object") {
            const combined = Object.values(errorData)
                .map((value) =>
                    Array.isArray(value) ? value.join(" ") : String(value ?? "")
                )
                .join(" ");
            message.error(combined || "Не удалось выполнить операцию");
            return;
        }
        message.error("Не удалось выполнить операцию");
    };

    const handleSubmit = async () => {
        const trimmedTitle = infoTitle.trim();
        const trimmedName = infoName.trim();
        const trimmedValue = infoValue;

        if (!trimmedTitle || !trimmedName || !trimmedValue) {
            message.error("Заполните все обязательные поля");
            return;
        }

        setConfirmLoading(true);
        try {
            if (isEditMode && selectedStaticInformation) {
                await updateStatisticInformation(selectedStaticInformation.id, {
                    title: trimmedTitle,
                    name: trimmedName,
                    value: trimmedValue,
                    as_type: infoAsType,
                });
                message.success("Информация обновлена");
            } else {
                await createStatisticInformation({
                    title: trimmedTitle,
                    name: trimmedName,
                    value: trimmedValue,
                    as_type: infoAsType,
                });
                message.success("Информация добавлена");
            }
            onAction();
            setStaticInformationModalOpen(false);
            resetForm();
        } catch (error) {
            handleErrorResponse(error);
        } finally {
            setConfirmLoading(false);
        }
    };

    const handleCancel = () => {
        setStaticInformationModalOpen(false);
        resetForm();
    };

    const handleDelete = () => {
        if (!selectedStaticInformation) {
            return;
        }
        setDeleteConfirmVisible(true);
    };

    const handleDeleteConfirm = async () => {
        if (!selectedStaticInformation) {
            return;
        }

        setDeleteLoading(true);
        try {
            await deleteStatisticInformation(selectedStaticInformation.id);
            message.success("Информация удалена");
            onAction();
            setDeleteConfirmVisible(false);
            setStaticInformationModalOpen(false);
            resetForm();
        } catch (error) {
            handleErrorResponse(error);
        } finally {
            setDeleteLoading(false);
        }
    };

    const handleTypeChange = (event: RadioChangeEvent) => {
        const newType = event.target.value as StaticInformationAvailableAsType;
        setInfoAsType(newType);
    };

    const renderValueInput = () => {
        const commonProps = {
            value: infoValue,
            onChange: (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
                setInfoValue(event.target.value),
        };

        switch (infoAsType) {
            case "boolean":
                return (
                    <Radio.Group
                        value={infoValue}
                        onChange={(event) => setInfoValue(event.target.value)}
                        className="mt-2"
                    >
                        <div className="grid grid-cols-2 gap-2">
                            <Radio.Button value="true">True</Radio.Button>
                            <Radio.Button value="false">False</Radio.Button>
                        </div>
                    </Radio.Group>
                );
            case "json":
                return (
                    <Input.TextArea
                        {...commonProps}
                        placeholder="Введите JSON"
                        autoSize={{ minRows: 4, maxRows: 6 }}
                    />
                );
            case "number":
            case "float":
                return (
                    <Input
                        {...commonProps}
                        type="number"
                        placeholder="Введите число"
                    />
                );
            case "date":
                return (
                    <Input
                        {...commonProps}
                        type="date"
                    />
                );
            case "time":
                return (
                    <Input
                        {...commonProps}
                        type="time"
                    />
                );
            case "datetime":
                return (
                    <Input
                        {...commonProps}
                        type="datetime-local"
                    />
                );
            default:
                return (
                    <Input
                        {...commonProps}
                        placeholder="Введите значение"
                    />
                );
        }
    };

    const modalTitle = isEditMode ? "Изменение информации" : "Новая информация";
    const primaryButtonText = isEditMode ? "Изменить" : "Добавить";

    const footerButtons: React.ReactNode[] = [
        <Button key="cancel" onClick={handleCancel}>
            Отмена
        </Button>,
    ];

    if (isEditMode) {
        footerButtons.push(
            <Button key="delete" danger onClick={handleDelete}>
                Удалить
            </Button>
        );
    }

    footerButtons.push(
        <Button
            key="submit"
            type="primary"
            loading={confirmLoading}
            onClick={handleSubmit}
        >
            {primaryButtonText}
        </Button>
    );

    return (
        <>
            <Modal
                title={modalTitle}
                open={staticInformationModalOpen}
                onCancel={handleCancel}
                footer={footerButtons}
            >
                <div className="mb-3">
                    <label className="block mb-1">Человекочитаемое название</label>
                    <Input
                        placeholder="Человекочитаемое название"
                        value={infoTitle}
                        onChange={(event) => setInfoTitle(event.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <label className="block mb-1">Ключ API</label>
                    <Input
                        placeholder="Ключ API"
                        value={infoName}
                        onChange={(event) => setInfoName(event.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <label className="block mb-1">Тип данных</label>
                    <Radio.Group value={infoAsType} onChange={handleTypeChange}>
                        <div className="grid grid-cols-4 gap-2 mt-2">
                            {typeOptions.map((option) => (
                                <Radio.Button key={option.value} value={option.value}>
                                    {option.label}
                                </Radio.Button>
                            ))}
                        </div>
                    </Radio.Group>
                </div>
                <div className="mb-3">
                    <label className="block mb-1">Значение</label>
                    {renderValueInput()}
                </div>
            </Modal>
            <Modal
                open={deleteConfirmVisible}
                title="Удаление информации"
                okText="Удалить"
                okButtonProps={{ danger: true, loading: deleteLoading }}
                cancelText="Отмена"
                onOk={handleDeleteConfirm}
                onCancel={() => {
                    if (!deleteLoading) {
                        setDeleteConfirmVisible(false);
                    }
                }}
                centered
            >
                <p>Удалить запись «{selectedStaticInformation?.title}»?</p>
            </Modal>
        </>
    );
};

export default StaticInformationModal;
