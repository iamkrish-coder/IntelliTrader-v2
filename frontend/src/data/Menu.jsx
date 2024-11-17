import React from 'react';
import { FaChartPie, FaWallet, FaExchangeAlt, FaHistory, FaRegLightbulb, FaPlus, FaCog } from 'react-icons/fa';

const DashboardMenu = [
    {
        "label": "Portfolio Overview",
        "link": "/dashboard/overview",
        "icon": <FaWallet className="mr-2"/>,
    },
    {
        "label": "Current Trades",
        "link": "/dashboard/trades",
        "icon": <FaExchangeAlt className="mr-2"/>,
    },
    {
        "label": "Trade History",
        "link": "/dashboard/history",
        "icon": <FaHistory className="mr-2"/>,
    },
]

const StrategyMenu = [
    {
        "label": "View Strategies",
        "link": "/strategy/settings",
        "icon": <FaRegLightbulb className="mr-2"/>,
    },
    {
        "label": "Create Strategies",
        "link": "/strategy/create",
        "icon": <FaPlus className="mr-2"/>,
    },
]

const ConfigurationMenu = [ 
    {
        "label": "Setup Configuration",
        "link": "/configuration/setup",
        "icon": <FaCog className="mr-2"/>,
    }
]

export { DashboardMenu, StrategyMenu, ConfigurationMenu };
