import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


def get_all_properties():
    properties = cache.get('all_properties')
    if not properties:
        properties = list(Property.objects.all().values())
        cache.set('all_properties', properties, 3600)  # cache for 1 hour
    return properties


def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info("stats")

    keyspace_hits = info.get("keyspace_hits", 0)
    keyspace_misses = info.get("keyspace_misses", 0)

    total_requests = keyspace_hits + keyspace_misses
    hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0

    logger.error(f"Redis Cache Metrics -> Hits: {keyspace_hits}, Misses: {keyspace_misses}, Hit Ratio: {hit_ratio}")

    return {
        "keyspace_hits": keyspace_hits,
        "keyspace_misses": keyspace_misses,
        "hit_ratio": hit_ratio,
    }
