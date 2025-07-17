// Custom JavaScript for Flask Graph Management System

$(document).ready(function() {
    // Initialize toastr options
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Confirm delete actions
    $('.delete-btn').click(function(e) {
        e.preventDefault();
        var form = $(this).closest('form');
        var itemName = $(this).data('item-name') || 'este elemento';
        
        if (confirm('¿Estás seguro de que quieres eliminar ' + itemName + '?')) {
            form.submit();
        }
    });

    // Form validation
    $('form').submit(function(e) {
        var requiredFields = $(this).find('[required]');
        var isValid = true;
        
        requiredFields.each(function() {
            if ($(this).val() === '') {
                $(this).addClass('is-invalid');
                isValid = false;
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            toastr.error('Por favor, complete todos los campos obligatorios');
        }
    });

    // Remove validation errors on input
    $('input, select, textarea').on('input change', function() {
        $(this).removeClass('is-invalid');
    });

    // Loading spinner for forms
    $('form').submit(function() {
        var submitBtn = $(this).find('button[type="submit"]');
        submitBtn.prop('disabled', true);
        submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Procesando...');
        
        // Re-enable button after 10 seconds (in case of error)
        setTimeout(function() {
            submitBtn.prop('disabled', false);
            submitBtn.html(submitBtn.data('original-text') || 'Enviar');
        }, 10000);
    });

    // Store original button text
    $('button[type="submit"]').each(function() {
        $(this).data('original-text', $(this).html());
    });

    // Dynamic city selection based on province
    $('#provincia_id').change(function() {
        var provinciaId = $(this).val();
        var ciudadSelect = $('#ciudad_origen_id, #ciudad_destino_id');
        
        if (provinciaId) {
            $.ajax({
                url: '/grafo/api/ciudades/' + provinciaId,
                type: 'GET',
                success: function(data) {
                    ciudadSelect.empty();
                    ciudadSelect.append('<option value="">Seleccione una ciudad</option>');
                    $.each(data, function(index, ciudad) {
                        ciudadSelect.append('<option value="' + ciudad.id + '">' + ciudad.nombre + '</option>');
                    });
                },
                error: function() {
                    toastr.error('Error al cargar ciudades');
                }
            });
        } else {
            ciudadSelect.empty();
            ciudadSelect.append('<option value="">Seleccione una ciudad</option>');
        }
    });

    // Search functionality
    $('#search-input').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $("#search-table tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Route calculation
    $('#route-form').submit(function(e) {
        e.preventDefault();
        
        var origen = $('#origen').val();
        var destino = $('#destino').val();
        var tipoRuta = $('#tipo_ruta').val();
        
        if (!origen || !destino) {
            toastr.error('Por favor, seleccione ciudades de origen y destino');
            return;
        }
        
        if (origen === destino) {
            toastr.error('La ciudad de origen y destino no pueden ser la misma');
            return;
        }
        
        // Show loading
        $('.loading-spinner').show();
        $('#route-result').hide();
        
        // Submit form normally
        this.submit();
    });

    // Real-time statistics update
    function updateStats() {
        $.ajax({
            url: '/grafo/api/stats',
            type: 'GET',
            success: function(data) {
                $('#total-cities').text(data.total_cities);
                $('#total-routes').text(data.total_routes);
                $('#coastal-cities').text(data.coastal_cities);
                $('#connectivity').text(data.connectivity_percentage + '%');
            },
            error: function() {
                console.log('Error updating statistics');
            }
        });
    }

    // Update stats every 30 seconds if on dashboard
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
        setInterval(updateStats, 30000);
    }

    // Initialize DataTables if available
    if ($.fn.DataTable) {
        $('.data-table').DataTable({
            responsive: true,
            lengthChange: false,
            autoWidth: false,
            pageLength: 10,
            language: {
                search: "Buscar:",
                lengthMenu: "Mostrar _MENU_ registros por página",
                zeroRecords: "No se encontraron resultados",
                info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
                infoEmpty: "Mostrando 0 a 0 de 0 registros",
                infoFiltered: "(filtrado de _MAX_ registros totales)",
                paginate: {
                    first: "Primero",
                    last: "Último",
                    next: "Siguiente",
                    previous: "Anterior"
                }
            }
        });
    }

    // Auto-refresh graph visualization
    function refreshGraph() {
        var graphContainer = $('#graph-container');
        if (graphContainer.length) {
            $.ajax({
                url: window.location.href,
                type: 'GET',
                success: function(data) {
                    var newGraph = $(data).find('#graph-container').html();
                    if (newGraph) {
                        graphContainer.html(newGraph);
                    }
                },
                error: function() {
                    console.log('Error refreshing graph');
                }
            });
        }
    }

    // Refresh graph every 60 seconds if on visualization page
    if (window.location.pathname.includes('/grafo/visualizar')) {
        setInterval(refreshGraph, 60000);
    }

    // Mobile menu toggle
    $('.navbar-toggler').click(function() {
        $('.navbar-collapse').toggleClass('show');
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').click(function(e) {
        e.preventDefault();
        var target = $($(this).attr('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 500);
        }
    });

    // Copy to clipboard functionality
    $('.copy-btn').click(function() {
        var text = $(this).data('copy-text');
        navigator.clipboard.writeText(text).then(function() {
            toastr.success('Copiado al portapapeles');
        }, function() {
            toastr.error('Error al copiar');
        });
    });

    // Print functionality
    $('.print-btn').click(function() {
        window.print();
    });

    // Export functionality
    $('.export-btn').click(function() {
        var format = $(this).data('format');
        var table = $('.data-table').DataTable();
        
        if (format === 'csv') {
            table.buttons.exportData({ format: 'csv' });
        } else if (format === 'pdf') {
            table.buttons.exportData({ format: 'pdf' });
        }
    });
});

// Utility functions
function showLoading() {
    $('.loading-spinner').show();
}

function hideLoading() {
    $('.loading-spinner').hide();
}

function showError(message) {
    toastr.error(message);
}

function showSuccess(message) {
    toastr.success(message);
}

function showInfo(message) {
    toastr.info(message);
}

function showWarning(message) {
    toastr.warning(message);
}

// Format distance
function formatDistance(distance) {
    return parseFloat(distance).toFixed(1) + ' km';
}

// Format time
function formatTime(time) {
    if (time < 1) {
        return (time * 60).toFixed(0) + ' min';
    } else {
        return time.toFixed(1) + ' h';
    }
}

// Validate email format
function validateEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate password strength
function validatePassword(password) {
    // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    var re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/;
    return re.test(password);
}
