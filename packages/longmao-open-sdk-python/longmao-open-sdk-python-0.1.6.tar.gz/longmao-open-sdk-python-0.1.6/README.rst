longmao-open-sdk-python
==================

The official LongMao SDK for Python.

访问龙猫数据开放平台的官方SDK。


Links
-----

* Website: https://www.longmaosoft.com


Example
----------------

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    import logging
    import traceback

    from longmao.api.project.ApiProjectTaskCreate import ApiProjectTaskCreate
    from longmao.core.DefaultLongMaoClient import DefaultLongMaoClient
    from longmao.core.LongMaoClientConfig import LongMaoClientConfig

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        filemode='a',)
    logger = logging.getLogger('')


    if __name__ == '__main__':
        """
        设置配置。
        """
        longmao_client_config = LongMaoClientConfig()
        longmao_client_config.access_key_id = '58bf489978ed44c49a4b9c64e96d9d6f'
        longmao_client_config.access_key_secret = 'bacb00c2e0200ccd7e997b53c9efb62d795b70e9'

        """
        得到客户端对象。
        """
        client = DefaultLongMaoClient(longmao_client_config, logger)

        """
        系统接口示例：批量添加任务
        """
        # 对照接口文档，构造请求对象
        api = ApiProjectTaskCreate()
        api.project_id = 'd36ec84f-ea18-4d1d-ae33-33bbad816f11'
        api.file = {'file': open('/longmao/data/demo.csv', 'rb')}

        result = None
        try:
            result = client.execute(api)
        except Exception as e:
            print(traceback.format_exc())
        if not result:
            print("failed execute")
        else:
            if result['code'] == '200':
                # 成功
                print("get response job_id:" + result['object']['job_id'])
            else:
                # 失败
                print(result['code'] + "," + result['message'])
