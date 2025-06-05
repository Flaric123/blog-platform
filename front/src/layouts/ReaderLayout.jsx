import { Layout } from "antd"
import { Outlet } from "react-router"
import withAccessCheck from "../hoc/withAccessCheck"
import { ROLES } from "../consts"


function ReaderLayout(){
    return(
        <Layout>
            <Layout.Header style={{ display: 'flex', alignItems: 'center', color:"black"}}>

            </Layout.Header>
            <Layout.Content>
                <Outlet/>
            </Layout.Content>
        </Layout>
    )
}

export default withAccessCheck(ReaderLayout,[ROLES.READER.NAME])