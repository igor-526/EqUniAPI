export const getPaginationValues = (pageNumber: number, pageSize: number) => {
    return {
        offset: ((pageNumber - 1) * pageSize),
        limit: pageSize
    }
}