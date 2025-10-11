type HorseOwnerTypeType = 0 | 1 | 2;

export type HorseOwnerType = {
    id: number
    name: string
    description: string
    type: HorseOwnerTypeType
    address: string[]
    phone_number: string[]
}