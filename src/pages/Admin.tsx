import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';
import Icon from '@/components/ui/icon';

interface Booking {
  id: number;
  user_id: number;
  username: string;
  first_name: string;
  check_in: string;
  check_out: string;
  price: number;
  status: string;
  created_at: string;
}

const Admin = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const response = await fetch('https://functions.poehali.dev/febc0c67-6280-475a-8a02-9b5dd08273b4');
      const data = await response.json();
      
      if (data.success) {
        setBookings(data.bookings);
      }
    } catch (error) {
      toast({
        title: 'Ошибка',
        description: 'Не удалось загрузить бронирования',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (bookingId: number, newStatus: string) => {
    try {
      const response = await fetch('https://functions.poehali.dev/febc0c67-6280-475a-8a02-9b5dd08273b4', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ booking_id: bookingId, status: newStatus })
      });
      
      const data = await response.json();
      
      if (data.success) {
        toast({
          title: 'Успешно',
          description: 'Статус обновлён'
        });
        fetchBookings();
      }
    } catch (error) {
      toast({
        title: 'Ошибка',
        description: 'Не удалось обновить статус',
        variant: 'destructive'
      });
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  const getStatusBadge = (status: string) => {
    const variants: Record<string, { variant: 'default' | 'secondary' | 'destructive' | 'outline', label: string }> = {
      pending: { variant: 'secondary', label: 'Ожидает' },
      confirmed: { variant: 'default', label: 'Подтверждено' },
      cancelled: { variant: 'destructive', label: 'Отменено' }
    };
    
    const config = variants[status] || { variant: 'outline', label: status };
    return <Badge variant={config.variant}>{config.label}</Badge>;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
        <div className="text-center">
          <Icon name="Loader2" className="animate-spin h-12 w-12 mx-auto text-slate-600 mb-4" />
          <p className="text-slate-600">Загрузка...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-slate-900 mb-2">Админ-панель</h1>
              <p className="text-slate-600">Управление бронированиями квартиры</p>
            </div>
            <Button onClick={fetchBookings} variant="outline" className="gap-2">
              <Icon name="RefreshCw" size={16} />
              Обновить
            </Button>
          </div>
        </div>

        <div className="grid gap-6 mb-8 md:grid-cols-3">
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Всего бронирований</CardDescription>
              <CardTitle className="text-3xl">{bookings.length}</CardTitle>
            </CardHeader>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Ожидают подтверждения</CardDescription>
              <CardTitle className="text-3xl">
                {bookings.filter(b => b.status === 'pending').length}
              </CardTitle>
            </CardHeader>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Подтверждено</CardDescription>
              <CardTitle className="text-3xl">
                {bookings.filter(b => b.status === 'confirmed').length}
              </CardTitle>
            </CardHeader>
          </Card>
        </div>

        <div className="space-y-4">
          {bookings.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <Icon name="Inbox" className="h-12 w-12 mx-auto text-slate-400 mb-4" />
                <p className="text-slate-600">Пока нет бронирований</p>
              </CardContent>
            </Card>
          ) : (
            bookings.map((booking) => (
              <Card key={booking.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <CardTitle className="flex items-center gap-2">
                        <Icon name="User" size={20} />
                        {booking.first_name}
                        {booking.username && (
                          <span className="text-sm font-normal text-slate-500">
                            @{booking.username}
                          </span>
                        )}
                      </CardTitle>
                      <CardDescription>
                        Бронирование #{booking.id} • {new Date(booking.created_at).toLocaleString('ru-RU')}
                      </CardDescription>
                    </div>
                    {getStatusBadge(booking.status)}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-2 mb-4">
                    <div className="flex items-center gap-2">
                      <Icon name="Calendar" className="text-slate-500" size={18} />
                      <div>
                        <p className="text-sm text-slate-500">Заезд</p>
                        <p className="font-medium">{new Date(booking.check_in).toLocaleDateString('ru-RU')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <Icon name="Calendar" className="text-slate-500" size={18} />
                      <div>
                        <p className="text-sm text-slate-500">Выезд</p>
                        <p className="font-medium">{new Date(booking.check_out).toLocaleDateString('ru-RU')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <Icon name="Wallet" className="text-slate-500" size={18} />
                      <div>
                        <p className="text-sm text-slate-500">Стоимость</p>
                        <p className="font-medium text-lg">{booking.price}₽</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <Icon name="MessageSquare" className="text-slate-500" size={18} />
                      <div>
                        <p className="text-sm text-slate-500">Telegram ID</p>
                        <p className="font-medium">{booking.user_id}</p>
                      </div>
                    </div>
                  </div>

                  {booking.status === 'pending' && (
                    <div className="flex gap-2">
                      <Button 
                        onClick={() => updateStatus(booking.id, 'confirmed')}
                        className="flex-1 gap-2"
                      >
                        <Icon name="Check" size={16} />
                        Подтвердить
                      </Button>
                      <Button 
                        onClick={() => updateStatus(booking.id, 'cancelled')}
                        variant="destructive"
                        className="flex-1 gap-2"
                      >
                        <Icon name="X" size={16} />
                        Отменить
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Admin;
