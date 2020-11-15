
'''
路由配置
'''

routes = [
    {
        'path': '/device',
        'name': 'device',
        'label': '设备管理',
        'icon': 'navbar_home.png',
        'redirect': { 'name': 'DeviceList' },
        'children': [
            { 'path': 'list', 'name': 'DeviceList' },
            { 'path': 'monitor', 'name': 'DeviceMonitor' },
        ]
    }, {
        'path': '/datum',
        'name': 'datum',
        'label': '数据管理',
        'icon': 'navbar_analysis.png',
        'redirect': { 'name': 'DatumAnalysis' },
        'children': [
            { 'path': 'analysis', 'name': 'DatumAnalysis' },
            { 'path': 'query', 'name': 'DatumQuery' },
        ]
    }, {
        'path': '/setting',
        'name': 'setting',
        'label': '配置管理',
        'icon': 'navbar_setting.png',
        'redirect': { 'name': 'SettingIndex' },
        'children': [
            { 'path': 'index', 'name': 'SettingIndex' },
        ]
    }
]

menus = [
    {
        'path': '/device',
        'children': [
            { 'path': '/device/list', 'name': 'DeviceList', 'label': '设备列表', 'icon': 'fa5s.list' },
            { 'path': '/device/monitor', 'name': 'DeviceMonitor', 'label': '设备监控', 'icon': 'fa5s.desktop' },
        ]
    }, {
        'path': '/datum',
        'children': [
            { 'path': '/datum/analysis', 'name': 'DatumAnalysis', 'label': '数据分析', 'icon': 'fa5s.chart-line' },
            { 'path': '/datum/query', 'name': 'DatumQuery', 'label': '数据查询', 'icon': 'fa5s.memory' },
        ]
    }
]