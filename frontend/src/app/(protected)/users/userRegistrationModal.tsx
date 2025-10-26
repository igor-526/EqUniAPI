import React, { ChangeEvent, useCallback, useEffect, useState } from 'react';
import { Input, Modal, message } from 'antd';
import { GetUserRegistrationModalElementType } from '@/types/ui/staticInformationModal';
import { registerUser } from '@/api/users';
import type { UserRegistrationInDtoType } from '@/types/api/users';

const transliterationMap: Record<string, string> = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ь": "",
    "ы": "y",
    "ъ": "",
    "э": "e",
    "ю": "yu",
    "я": "ya"
};

const transliterate = (value: string): string =>
    value
        .toLowerCase()
        .split("")
        .map((char) => transliterationMap[char] ?? char)
        .join("");

const buildAutoUsername = (lastName: string, firstName: string): string => {
    const sanitizedLastName = transliterate(lastName).replace(/[^a-z0-9]/g, "");
    const sanitizedFirstName = transliterate(firstName).replace(/[^a-z0-9]/g, "");
    if (!sanitizedLastName && !sanitizedFirstName) {
        return "";
    }
    if (!sanitizedLastName) {
        return sanitizedFirstName ? sanitizedFirstName[0] : "";
    }
    if (!sanitizedFirstName) {
        return sanitizedLastName;
    }
    return `${sanitizedLastName}.${sanitizedFirstName[0]}`;
};

const generateRandomPassword = (length = 8): string => {
    const characters = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789";
    let result = "";
    for (let i = 0; i < length; i += 1) {
        const index = Math.floor(Math.random() * characters.length);
        result += characters[index];
    }
    return result;
};

const UserRegistrationModal: GetUserRegistrationModalElementType = ({
    registrationModalOpen,
    setRegistrationModalOpen,
    onRegistered
}) => {
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [usernameManuallyEdited, setUsernameManuallyEdited] = useState(false);
    const [newUserLastName, setNewUserLastName] = useState("");
    const [newUserFirstName, setNewUserFirstName] = useState("");
    const [newUserPatronymic, setNewUserPatronymic] = useState("");
    const [newUserUsername, setNewUserUsername] = useState("");
    const [newUserEmail, setNewUserEmail] = useState("");
    const [newUserPassword, setNewUserPassword] = useState("");

    const initializeForm = useCallback(() => {
        setNewUserLastName("");
        setNewUserFirstName("");
        setNewUserPatronymic("");
        setNewUserUsername("");
        setNewUserEmail("");
        setNewUserPassword(generateRandomPassword());
        setUsernameManuallyEdited(false);
        setConfirmLoading(false);
    }, []);

    useEffect(() => {
        if (registrationModalOpen) {
            initializeForm();
        }
    }, [registrationModalOpen, initializeForm]);

    useEffect(() => {
        if (!usernameManuallyEdited) {
            setNewUserUsername(buildAutoUsername(newUserLastName, newUserFirstName));
        }
    }, [newUserLastName, newUserFirstName, usernameManuallyEdited]);

    const handleLastNameChange = (event: ChangeEvent<HTMLInputElement>) => {
        setNewUserLastName(event.target.value);
    };

    const handleFirstNameChange = (event: ChangeEvent<HTMLInputElement>) => {
        setNewUserFirstName(event.target.value);
    };

    const handlePatronymicChange = (event: ChangeEvent<HTMLInputElement>) => {
        setNewUserPatronymic(event.target.value);
    };

    const handleUsernameChange = (event: ChangeEvent<HTMLInputElement>) => {
        setUsernameManuallyEdited(true);
        setNewUserUsername(event.target.value);
    };

    const handleEmailChange = (event: ChangeEvent<HTMLInputElement>) => {
        setNewUserEmail(event.target.value);
    };

    const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
        setNewUserPassword(event.target.value);
    };

    const handleOk = async () => {
        setConfirmLoading(true);

        const trimmedFirstName = newUserFirstName.trim();
        const trimmedLastName = newUserLastName.trim();
        const trimmedUsername = newUserUsername.trim();

        if (!trimmedLastName || !trimmedFirstName || !trimmedUsername || !newUserPassword) {
            message.error("Заполните обязательные поля: фамилия, имя, username и пароль");
            setConfirmLoading(false);
            return;
        }

        const payload: UserRegistrationInDtoType = {
            first_name: trimmedFirstName,
            last_name: trimmedLastName,
            username: trimmedUsername,
            password: newUserPassword
        };

        const trimmedPatronymic = newUserPatronymic.trim();
        if (trimmedPatronymic) {
            payload.patronymic = trimmedPatronymic;
        }

        const trimmedEmail = newUserEmail.trim();
        if (trimmedEmail) {
            payload.email = trimmedEmail;
        }

        try {
            await registerUser(payload);
            message.success("Пользователь успешно зарегистрирован");
            onRegistered();
            setRegistrationModalOpen(false);
            initializeForm();
        } catch (error: any) {
            const errorData = error?.response?.data;
            if (typeof errorData === "string") {
                message.error(errorData);
            } else if (errorData && typeof errorData === "object") {
                const messages = Object.values(errorData as Record<string, unknown>)
                    .map((value) =>
                        Array.isArray(value) ? value.join(" ") : String(value ?? "")
                    )
                    .join(" ");
                message.error(messages || "Не удалось зарегистрировать пользователя");
            } else {
                message.error("Не удалось зарегистрировать пользователя");
            }
        } finally {
            setConfirmLoading(false);
        }
    };

    const handleCancel = () => {
        setRegistrationModalOpen(false);
        initializeForm();
    };

    return (
        <Modal
            title="Новый пользователь"
            open={registrationModalOpen}
            okText="Зарегистрировать"
            onOk={handleOk}
            confirmLoading={confirmLoading}
            onCancel={handleCancel}
        >
            <div className="mb-3">
                <label>Фамилия</label>
                <Input
                    placeholder="Фамилия"
                    value={newUserLastName}
                    onChange={handleLastNameChange}
                />
            </div>

            <div className="mb-3">
                <label>Имя</label>
                <Input
                    placeholder="Имя"
                    value={newUserFirstName}
                    onChange={handleFirstNameChange}
                />
            </div>

            <div className="mb-3">
                <label>Отчество</label>
                <Input
                    placeholder="Отчество"
                    value={newUserPatronymic}
                    onChange={handlePatronymicChange}
                />
            </div>

            <div className="mb-3">
                <label>Username</label>
                <Input
                    placeholder="Username"
                    value={newUserUsername}
                    onChange={handleUsernameChange}
                />
            </div>

            <div className="mb-3">
                <label>Email</label>
                <Input
                    placeholder="Email"
                    type="email"
                    value={newUserEmail}
                    onChange={handleEmailChange}
                />
            </div>

            <div className="mb-3">
                <label>Пароль</label>
                <Input.Password
                    placeholder="Пароль"
                    value={newUserPassword}
                    onChange={handlePasswordChange}
                />
            </div>
        </Modal>
    );
};

export default UserRegistrationModal;
