export type BooleanFilterType = 'true' | 'false' | null | undefined;

export type ApiListPaginatedResponseType<T> = {
    count: number,
    items: T[]
}