import json
from tickets.models import Stadium, Sector, Place


def created_places(sender, instance, created, **kwargs):
    places_query = Stadium.objects.filter(pk=instance.pk).order_by().only("places").get()
    with open(places_query.places.path, "r") as places_file:
        places_data = json.load(places_file)
    places_list = []
    for side, sectors in places_data.items():
        for tribune, info in sectors.items():
            for sector, places in info.items():
                # print(f"Сторона на схеме: {side}, трибуна: {tribune}, номер сектора: {sector}, "
                #       f"количество рядов: {places.get('count_rows')}, кол-во мест: {places.get('places_in_rows')}")

                sector = Sector(sec_stadium=instance, name=f"{tribune}{sector}",
                                side=side)  # slug=slugify(f"{instance.slug} {tribune}{sector}"),
                sector.save()
                places_in_rows = places.get('places_in_rows')
                if len(places_in_rows) > 1:
                    for row_i, cnt_places in enumerate(places.get('places_in_rows'), 1):
                        for place_i in range(1, cnt_places+1):
                            place = Place(p_sector=sector, row=row_i, place=place_i)
                            places_list.append(place)
                else:
                    for row_i in range(1, places.get('count_rows')+1):
                        for place_i in range(1, places_in_rows[0]+1):
                            place = Place(p_sector=sector, row=row_i, place=place_i)
                            places_list.append(place)

    Place.objects.bulk_create(places_list)
