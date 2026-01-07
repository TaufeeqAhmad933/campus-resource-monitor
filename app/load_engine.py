from typing import List, Dict

OVERLOAD_THRESHOLD = 0.8
UNDERUTILIZED_THRESHOLD = 0.5


def analyze_load(resources: List[Dict]) -> Dict:
    overloaded = []
    underutilized = []

    for r in resources:
        load_ratio = r["current_load"] / r["max_capacity"]

        if load_ratio >= OVERLOAD_THRESHOLD:
            overloaded.append({**r, "load_ratio": load_ratio})

        elif load_ratio <= UNDERUTILIZED_THRESHOLD:
            underutilized.append({**r, "load_ratio": load_ratio})

    return {
        "overloaded": overloaded,
        "underutilized": underutilized
    }


def generate_recommendations(overloaded: List[Dict], underutilized: List[Dict]) -> List[Dict]:
    recommendations = []

    for o in overloaded:
        if not underutilized:
            continue

        # pick the most free resource
        target = min(underutilized, key=lambda x: x["load_ratio"])

        recommendations.append({
            "from": o["name"],
            "to": target["name"],
            "reason": f"{o['name']} is overloaded ({int(o['load_ratio']*100)}%), "
                      f"{target['name']} is underutilized ({int(target['load_ratio']*100)}%)"
        })

    return recommendations
