import { ReactNode } from "react"

type UserRegistrationModalPropsType = {
    registrationModalOpen: boolean
    setRegistrationModalOpen: (registrationModalOpen: boolean) => void
    onRegistered: () => void
}

export type GetUserRegistrationModalElementType = (props: UserRegistrationModalPropsType) => ReactNode
