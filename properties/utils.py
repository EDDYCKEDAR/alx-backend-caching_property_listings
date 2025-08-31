from django_redis import get_redis_connection

def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info("stats")
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0

    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio,
    }
