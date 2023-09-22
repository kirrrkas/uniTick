function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
        newElement.find(':input').each(function() {
        newElement.find(':input').each(function() {
            if(!$(this).attr('name').includes('match')){
                var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
                var id = 'id_' + name;
                $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
            } else {
                $(this).remove();
            }
        });
        newElement.find('label').each(function() {
            if(!($(this).attr('for')).includes('match')){
                var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
                $(this).attr('for', newFor);
            } else {
                $(this).remove();
            }
        });
//    }
    total++;
    $('#id_' + type + '-TOTAL_FORMS').value(total);
    $(selector).after(newElement);
    console.log(total, name);
}

$('#add_more').click(function() {
    cloneMore('formset:last', 'matchclub_set');
});

$('#add_more_tickets').click(function() {
    cloneMore('formset:last', 'tickets');
});


