import { ReactNode } from "react"
import { StaticInformationTableDataItemType } from "../api/static_information"

type StaticInformationModalPropsType = {
    staticInformationModalOpen: boolean
    setStaticInformationModalOpen: (staticInformationModalOpen: boolean) => void
    selectedStaticInformation: StaticInformationTableDataItemType | null
    onAction: () => void
}

export type GetStaticInformationModalElementType = (props: StaticInformationModalPropsType) => ReactNode
