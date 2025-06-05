import withAccessCheck from "../hoc/withAccessCheck"
import { Layout } from "antd"
import { Outlet } from "react-router"
import { ROLES } from "../consts"

function AdminLayout(){
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

export default withAccessCheck(AdminLayout,[ROLES.ADMIN.NAME])