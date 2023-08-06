from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.attr import AttrUtils
from celery import Celery

config = KubefacetsConfig().getConfig()
celeryConfig = DictUtils.get_by_path(config, "services.general.celery")
celeryInitConfig = DictUtils.get(celeryConfig, "init")
appName = DictUtils.get_by_path(config, "app")
celeryInitConfig["main"] = appName

celeryConfigAttr = AttrUtils.format(celeryInitConfig)

app = Celery(appName)
app.conf.update(**celeryInitConfig)
app.autodiscover_tasks()
