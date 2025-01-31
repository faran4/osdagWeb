import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import Home from "../pages/home/Home";
import Connection from "../pages/Modules/Connection";
import TensionMember from "../pages/Modules/TensionMember";
import CompressionMember from "../pages/Modules/CompressionMember";
import FlexuralMember from "../pages/Modules/FlexuralMember";
import BeamColumn from "../pages/Modules/BeamColumn";
import PlateGirder from "../pages/Modules/PlateGirder";
import Truss from "../pages/Modules/Truss";
import Frame2D from "../pages/Modules/Frame2D";
import Frame3D from "../pages/Modules/Frame3D";
import GroupDesign from "../pages/Modules/GroupDesign";
import Startpage from "../pages/home/Startpage";
import BeamBeamCoverPlate from "../pages/Modules/MomentConnection/BeamBeamCoverPlate";
import TestApi from "../components/TestApi";

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            {
                path: '/',
                element: <Home />,
                children: [
                    {
                        path: "/",
                        element: <Startpage />
                    },
                    {
                        path: "/connection",
                        element: <Connection />
                    },
                    {
                        path: "/tension-member",
                        element: <TensionMember />
                    },
                    {
                        path: "/compression-member",
                        element: <CompressionMember />
                    },
                    {
                        path: "/flexural-member",
                        element: <FlexuralMember />
                    },
                    {
                        path: "/beam-column",
                        element: <BeamColumn />
                    },
                    {
                        path: "/plate-girder",
                        element: <PlateGirder />
                    },
                    {
                        path: "/truss",
                        element: <Truss />
                    },
                    {
                        path: "/2d-frame",
                        element: <Frame2D />
                    },
                    {
                        path: "/3d-frame",
                        element: <Frame3D />
                    },
                    {
                        path: "/group-design",
                        element: <GroupDesign />
                    },
                ]
            }
        ]
    },
    {
        path: "/bbcoverplate",
        element: <BeamBeamCoverPlate />
    },
    {
        path: "/hello",
        element: <TestApi />
    }
]);

export default router;