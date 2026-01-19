import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import Icon from '@/components/ui/icon';

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="text-center px-4">
        <div className="mb-8">
          <Icon name="Home" className="h-24 w-24 mx-auto text-slate-700 mb-6" />
          <h1 className="text-5xl font-bold mb-4 text-slate-900">Аренда квартиры</h1>
          <p className="text-xl text-slate-600 mb-2">г. Мелитополь, Запорожская область</p>
          <p className="text-lg text-slate-500">Посуточная аренда • От 1500₽</p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button 
            size="lg"
            className="gap-2 text-lg px-8"
            onClick={() => window.open('https://t.me/Vgcidj', '_blank')}
          >
            <Icon name="MessageCircle" size={20} />
            Написать в Telegram
          </Button>
          
          <Button 
            size="lg"
            variant="outline"
            className="gap-2 text-lg px-8"
            onClick={() => navigate('/admin')}
          >
            <Icon name="Settings" size={20} />
            Админ-панель
          </Button>
        </div>
        
        <div className="mt-12 max-w-2xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <Icon name="Wifi" className="h-10 w-10 mx-auto text-slate-600 mb-2" />
              <p className="text-sm text-slate-600">Wi-Fi</p>
            </div>
            <div className="text-center">
              <Icon name="Bed" className="h-10 w-10 mx-auto text-slate-600 mb-2" />
              <p className="text-sm text-slate-600">Комфорт</p>
            </div>
            <div className="text-center">
              <Icon name="MapPin" className="h-10 w-10 mx-auto text-slate-600 mb-2" />
              <p className="text-sm text-slate-600">Центр</p>
            </div>
            <div className="text-center">
              <Icon name="Clock" className="h-10 w-10 mx-auto text-slate-600 mb-2" />
              <p className="text-sm text-slate-600">24/7</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;