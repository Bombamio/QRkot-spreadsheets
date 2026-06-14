from datetime import datetime


def close_object(obj):
    obj.fully_invested = True
    obj.close_date = datetime.now()


def invest(open_objects, target):
    updated_objects = []

    for obj in open_objects:
        available_obj = obj.full_amount - obj.invested_amount
        available_target = (
            target.full_amount - target.invested_amount
        )

        amount = min(available_obj, available_target)

        obj.invested_amount += amount
        target.invested_amount += amount

        updated_objects.append(obj)

        if obj.invested_amount == obj.full_amount:
            close_object(obj)

        if target.invested_amount == target.full_amount:
            close_object(target)
            break

    return updated_objects