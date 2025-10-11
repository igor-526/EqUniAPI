import { createSlice } from "@reduxjs/toolkit"

const layoutSlice = createSlice({
    name: "layout",
    initialState: {
        pageTitle: ""
    },
    reducers: {
        setNewTitle: (state, action) => {
            state.pageTitle = action.payload
        }
    }
})

export const { setNewTitle } = layoutSlice.actions

export default layoutSlice.reducer