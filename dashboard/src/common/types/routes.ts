import { routeTree } from "@marzneshin/routeTree.gen";
import { RoutePaths } from "@tanstack/react-router";

// We need to use both imports to define our router paths
export type AppRouterPaths = RoutePaths<typeof routeTree>;
