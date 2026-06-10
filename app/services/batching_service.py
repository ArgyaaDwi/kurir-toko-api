from datetime import datetime

from app.schemas.batching import BatchPlanItem, BatchPlanRequest, BatchPlanResponse
from app.schemas.order import OrderInput
from app.schemas.routing import BranchInput, OptimizeRouteRequest
from app.services.routing_service import optimize_routes


def _extract_order_minutes(order: OrderInput) -> int | None:
    if not order.order_date:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            parsed = datetime.strptime(order.order_date, fmt)
            return parsed.hour * 60 + parsed.minute
        except ValueError:
            continue
    return None


def _cutoff_to_minutes(cutoff_time: str) -> int:
    hour, minute = cutoff_time.split(":")
    return int(hour) * 60 + int(minute)


def plan_batches(request: BatchPlanRequest) -> BatchPlanResponse:
    grouped_orders: dict[str, list[OrderInput]] = {window.name: [] for window in request.windows}
    unparsed_orders: list[OrderInput] = []

    ordered_windows = sorted(request.windows, key=lambda window: _cutoff_to_minutes(window.cutoff_time))
    if not ordered_windows:
        return BatchPlanResponse(branch_code=request.branch_code, batch_count=0, batches=[])

    for order in request.orders:
        order_minutes = _extract_order_minutes(order)
        if order_minutes is None:
            unparsed_orders.append(order)
            continue

        assigned = False
        for window in ordered_windows:
            if order_minutes <= _cutoff_to_minutes(window.cutoff_time):
                grouped_orders[window.name].append(order)
                assigned = True
                break

        if not assigned:
            grouped_orders[ordered_windows[-1].name].append(order)

    if unparsed_orders:
        grouped_orders[ordered_windows[0].name].extend(unparsed_orders)

    batches = []
    for window in ordered_windows:
        batch_orders = grouped_orders[window.name]
        if not batch_orders:
            continue
        routing_result = optimize_routes(
            OptimizeRouteRequest(
                branch=BranchInput(code=request.branch_code),
                orders=batch_orders,
                kurir_toko_only=request.kurir_toko_only,
                algorithm=request.algorithm,
            )
        )
        batches.append(
            BatchPlanItem(
                batch_name=window.name,
                cutoff_time=window.cutoff_time,
                order_count=len(batch_orders),
                routing_result=routing_result,
            )
        )

    return BatchPlanResponse(
        branch_code=request.branch_code,
        batch_count=len(batches),
        batches=batches,
    )
