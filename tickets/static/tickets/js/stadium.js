function Stadium(){};
Stadium.prototype.Stage = null;
Stadium.prototype.Layer = null;
Stadium.prototype.CreateStage = function(width, height, backgroundUrl){
  console.debug('CreateStage');
  var settings = {
    container: 'container',
    width: width,
    height: height
  };

  this.Stage = new Kinetic.Stage(settings);
  this.Layer = new Kinetic.Layer();
  this.Stage.add(this.Layer);
  this.AddBackground(backgroundUrl);
};
Stadium.prototype.CreateCompleted = function(){
  self.LoadSectors();
};
Stadium.prototype.AddBackground = function(backgroundUrl){
  console.debug('AddBackground', backgroundUrl);
  var self = this;
  var background = new Image();
  background.onload = function() {
    console.log('Background loaded');
    var settings = {
      image: background,
      width: background.width,
      height: background.height
    };
    var image = new Kinetic.Image(settings);
    image.on('mouseup', $.proxy(self.BackgroundMouseUp,self));
		self.Layer.add(image);
    image.moveToBottom();
    self.Layer.draw();
   	$.proxy(self.CreateCompleted(), self);
  };
  background.src = backgroundUrl;
};
Stadium.prototype.CreateSector = function(name, color, pathData){
  console.debug('CreateSector', name);
  var segments = this.GetPathSegments(pathData);
  var layer = this.Layer;
	var initialPosition = segments[0];
  var group =	new Kinetic.Group({x:initialPosition.x, y:initialPosition.y});

  var sector = new Kinetic.Shape({
    drawFunc: function (canvas) {

      var min = {x: layer.parent.getWidth(), y: layer.parent.getHeight()};
      var max = {x:0, y:0};

      var context = canvas.getContext();
      context.beginPath();

      for (var index = 0; index < segments.length; index++) {
        var seg = segments[index];

        if (seg.x <= min.x) min.x = seg.x;
        if (seg.y <= min.y) min.y = seg.y;
        if (seg.x >= max.x) max.x = seg.x;
        if (seg.y >= max.y) max.y = seg.y;

        switch(seg.pathSegTypeAsLetter){
          case 'M':
            context.moveTo(seg.x - initialPosition.x, seg.y - initialPosition.y);
            break;
          case 'C':
            context.bezierCurveTo(seg.x1 - initialPosition.x, seg.y1 - initialPosition.y, seg.x2 - initialPosition.x,seg.y2 - initialPosition.y, seg.x - initialPosition.x, seg.y - initialPosition.y);
            break;
          case 'L':
            context.lineTo(seg.x - initialPosition.x, seg.y - initialPosition.y);
            break;
          default:
            break;
        }
      }

      context.closePath();
      context.clip();
      context.fillStyle = this.getAttr('fill');
      context.fill();
      canvas.fillStroke(this);

      this.bound.min = min;
      this.bound.max = max;

      var center = {
        x:((max.x - min.x)/2) + min.x,
        y:((max.y - min.y)/2) + min.y
      };

      this.bound.center = center;
    },
    fill: color,
    strokeWidth: 0,
    opacity: 0.6
  });

  sector.bound = {min:null,max:null,center:null};
  sector.name = name;
  sector.overDisabled = false;

  sector.on('mouseover', $.proxy(this.SectorMouseOver, this));
  sector.on('mouseout', $.proxy(this.SectorMouseOut, this));
  sector.on('mouseup', $.proxy(this.SectorMouseUp, this));

  group.add(sector);

  this.Layer.add(group);
  this.Layer.draw();
  return sector;
};
Stadium.prototype.CreateSeat = function(name, sector, position, products){
  var settings = {
    x: position.x,
    y: position.y,
    radius: 1,
    fill: 'gray',
    stroke: 'white',
    strokeWidth: '0.4',
    opacity: 0.6
  };
  var seat = new Kinetic.Circle(settings);
  seat.name = name;
  seat.products = products;

  seat.on('mouseover', $.proxy(this.SeatMouseOver, this));
  seat.on('mouseout', $.proxy(this.SeatMouseOut, this));
  seat.on('mouseup', $.proxy(this.SeatMouseUp, this));

  var group = sector.parent;
  group.add(seat);
  group.parent.draw();
};
Stadium.prototype.BackgroundMouseUp = function(e){

  var min = {x:0, y:0};
  var max = {x:this.Stage.getWidth(), y:this.Stage.getHeight()};
  var center = {
    x:((max.x - min.x)/2) + min.x,
    y:((max.y - min.y)/2) + min.y
  };
  var defaultRect = {min:min, max:max, center:center};
  this.Zoom(defaultRect);


};
Stadium.prototype.SectorMouseOver = function(e){
  document.body.style.cursor = 'pointer';
  var sender = e.targetNode;
  if (sender.overDisabled == false)
  {
    sender.setOpacity(0.1);
    sender.parent.parent.draw();
  }
};
Stadium.prototype.SectorMouseOut = function(e){
  document.body.style.cursor = 'default';
  var sender = e.targetNode;
  if (sender.overDisabled == false)
  {
    sender.setOpacity(0.6);
    sender.parent.parent.draw();
  }
};
Stadium.prototype.SectorMouseUp = function(e){
  var sender = e.targetNode;
  this.UnloadByType('Rect');
  this.UnloadByType('Line');
  this.UnloadByType('Text');
  if (sender.overDisabled == false)
  {
    this.Zoom(sender.bound, $.proxy(this.LoadSectorSeats, this, sender ));
    sender.overDisabled = true;
  }
};
Stadium.prototype.SeatMouseOver = function(e){
  document.body.style.cursor = 'pointer';
  var sender = e.targetNode;
  sender.setOpacity(1);
  sender.parent.draw();
};
Stadium.prototype.SeatMouseOut = function(e){
  document.body.style.cursor = 'default';
  var sender = e.targetNode;
  sender.setOpacity(0.6);
  sender.parent.draw();
};
Stadium.prototype.SeatMouseUp = function(e){
  var sender = e.targetNode;
  this.SeatClicked(sender);
};
Stadium.prototype.SeatClicked = function(seat){
  this.LoadSeatProducts(seat);
};
Stadium.prototype.LoadSectors = function(){};
Stadium.prototype.LoadSectorSeats = function(){};
Stadium.prototype.LoadSeatProducts = function(seat) {
  this.UnloadByType('Rect');
  this.UnloadByType('Line');
  this.UnloadByType('Text');

  var products = seat.products;
  var group = seat.parent;
  var position = seat.getPosition();
	var productSettings = {
    x: 0,
    y: 0,
    width: 17,
    height: 5,
    fill: '#4c6281',
    stroke: 'white',
    strokeWidth: 0.1,
    shadowColor: 'black',
    shadowBlur: 10,
    shadowOffset: {x:10,y:10},
    shadowOpacity: 0.2,
    cornerRadius: 1,
    opacity: 0.7

  };
  var lineSettings = {
    points: [0,0,0,0],
    stroke: 'gray',
    strokeWidth: 0.2
  };
  var labelSettings = {
    x: 0,
    y: 0,
    text: '',
    fontSize: 3,
    fontFamily: 'Arial',
    fill: 'white'
  };

  var radius = 10;
  var stepAngle = 360 / products.length;

  for (var index in products) {
    var data = products[index];
    var product = new Kinetic.Rect(productSettings);
    //var line = new Kinetic.Line(lineSettings);
    var label = new Kinetic.Text(labelSettings);
    //group.add(line);
    group.add(product);
    group.add(label);

    var angle = (index * stepAngle) + 68;
    var x = (Math.sin(angle * (Math.PI/180)) * radius) + position.x;
    var y = (Math.cos(angle * (Math.PI/180)) * radius) + position.y;
    product.name = data.name;
    //product.setX(x - (productSettings.width /2));
    //product.setY(y - (productSettings.height /2));
		//label.setX(product.getX() + 1);
    //label.setY(product.getY() + 1);
		label.setText(product.name);
    //line.setPoints([position.x, position.y, x, y ]);
    //group.parent.draw();


    //Test (ugly performance)
    $(product.attrs).animate(
      {
        x: x - (productSettings.width /2),
        y: y - (productSettings.height /2)
      },
      {
      duration: 500,
      step: function (value) {
        group.parent.draw();
      }
    }
    );

    $(label.attrs).animate(
      {
        x: x - (productSettings.width /2) + 1,
        y: y - (productSettings.height /2) + 1
      },
      {
      duration: 500,
      step: function (value) {
        group.parent.draw();
      }
    }
    );
  }
};
Stadium.prototype.UnloadSectorSeats = function(sector){
  console.log('UnloadSectors');

  var allSectors = this.Stage.get('Shape');
  for (var index = 0; index < allSectors.length; index++) {
		allSectors[index].overDisabled = false;
    allSectors[index].setOpacity(0.6);
  	allSectors[index].parent.parent.draw();
  }

  this.UnloadByType('Circle');
  this.UnloadByType('Rect');
  this.UnloadByType('Line');
  this.UnloadByType('Text');

};
Stadium.prototype.UnloadByType = function(type){
  var typedObjects = this.Stage.get(type);
  for (var index = 0; index < typedObjects.length; index++) {
		typedObjects[index].remove();
  }
  this.Stage.draw();
};
Stadium.prototype.GetBoundingLength = function(boundingRect){
  var width = Math.abs(boundingRect.max.x - boundingRect.min.x);
  var height = Math.abs(boundingRect.max.y - boundingRect.min.y);
  var bounding = {width:width, height:height};
  return bounding;
};
Stadium.prototype.Zoom = function(boundingRect, callback){
  //Dear God, i'm so sorry for these code lines.
  //I need to check if the the extra padding calculation is correct.
  this.UnloadSectorSeats();

  var padding = 10;
  var bdgLength = this.GetBoundingLength(boundingRect);
  var targetmaxlength = Math.max(bdgLength.width, bdgLength.height);
  var stagemaxlength = Math.max(this.Stage.getWidth(), this.Stage.getHeight());
  var maxlength = Math.max(targetmaxlength, stagemaxlength)+ (padding*2);
  var minlength = Math.min(targetmaxlength, stagemaxlength)+ (padding*2);

  var scaleFactor = maxlength/minlength;

	var stage = this.Stage;
  var zoomFrom = {
    x: stage.getX(),
    y:stage.getY(),
    scale: this.Stage.getScale().x
  };

  var centerpoint = boundingRect.center;
  centerpoint.x *= scaleFactor;
  centerpoint.y *= scaleFactor;
  centerpoint.x *= -1;
  centerpoint.y *= -1;
  centerpoint.x += this.Stage.getWidth()/2;
  centerpoint.y += this.Stage.getHeight()/2;

  var zoomTo = {
    x: centerpoint.x + (padding/2),
    y: centerpoint.y + (padding/2),
    scale: scaleFactor
  };

  $(zoomFrom).animate(zoomTo, {
    duration: 1000,
    easing : 'easeInOutQuart',
		step: function (value, event) {
      switch(event.prop){
        case 'scale':
          stage.setScale(value);
          break;
        case 'x':
          stage.setX(value);
          break;
        case 'y':
          stage.setY(value);
          break;
        default:
          break;
      }
      stage.draw();
    },
    complete: function(){
			if (callback){
        callback();
      }
    }
  });
};
Stadium.prototype.GetPathSegments = function(pathString){

  pathString = pathString.replace(/^\s+|\s+$/g, '');
  pathString = pathString.replace(/[\s\r\t\n]+/gm,' ');
  var parts = pathString.split(' ');
  var end = false;
  var index = 0;
  var segments = [];
  while (end == false) {
    var item = String(parts[index]);

    var cmdLetter = item.substring(0, 1).toUpperCase();;
    switch (cmdLetter){
      case "C":
        item = item.replace(cmdLetter, '');
        segments.push({
          pathSegTypeAsLetter:cmdLetter,
          x1:parseInt(item),
          y1:parseInt(parts[index + 1]),
          x2:parseInt(parts[index + 2]),
          y2:parseInt(parts[index + 3]),
          x:parseInt(parts[index + 4]),
          y:parseInt(parts[index + 5]),
        });
        index += 5;
        break;
      case "Z":
        index = parts.length;
        break;
      case "L":
      case "M":
      default:
        if (isNaN(cmdLetter))
          item = item.replace(cmdLetter, '');
        else
          cmdLetter='L';

        segments.push({
          pathSegTypeAsLetter:cmdLetter,
          x:parseInt(item),
          y:parseInt(parts[index + 1])
        });
        index += 1;
        break;
    }
    end = (index + 1 >= parts.length)? true: false;
    index++;
  }
  console.log(segments);
  return segments;

};

//External public methods below
var stadium = null;
$( document ).ready(function() {
  console.clear();
  stadium = new Stadium();

  //Configure
  stadium.LoadSectors = LoadSectors;
	stadium.LoadSectorSeats = LoadSectorSeats;
  //Init
  stadium.CreateStage(620, $(document).height(), 'http://footballtripper.com/wp-content/uploads/2014/08/king-power-stadium-leicester-city-seating-plan.jpg');
});
function LoadSectors(){
  //The PointData syntax is the same used to create an SVG path.
  //https://www.w3schools.com/svg/svg_path.asp
  //currently only works with "moveto","lineto", "curveto", "closepath"
  stadium.CreateSector('VS', '#0A4C80','M71 141 C71 141 69 29 198 29 L198 111 L163 111 C168 111 152 111 154 125 L154 141 Z');
  stadium.CreateSector('L1', '#7c2d88', 'M202 29 L229 29 229 111 202 111 Z');
  stadium.CreateSector('K1', '#3279b9', 'M233 29 L260 29 260 111 233 111 Z');
  stadium.CreateSector('J3', '#0a4c80', 'M264 29 L298 29 298 111 264 111 Z');
  stadium.CreateSector('J2', '#8ad3dc', 'M303 29 L337 29 338 111 302 111 Z');
  stadium.CreateSector('J1', '#0a4d81', 'M342 29 L375 29 377 111 342 111 Z');
  stadium.CreateSector('H1', '#3279b9', 'M382 29 L434 29 436 111 380 111 Z');
  stadium.CreateSector('G2', '#62a4d8', 'M439 29 L465 29 468 111 439 111 Z');
  stadium.CreateSector('G1', '#62a4d8', 'M470 29 C470 29 515 32 534 62 L478 115 C478 115 475 111 470 111 Z');
}
function LoadSectorSeats(sector) {
  var sample1 = [
    {id:1, name:'Product A'},
    {id:2, name:'Product B'},
    {id:3, name:'Product C'},
    {id:4, name:'Product D'}
  ];

  var sample2 = [
    {id:1, name:'Product 1'},
    {id:2, name:'Product 2'},
    {id:3, name:'Product 3'},
    {id:4, name:'Product 4'}
  ];
  stadium.CreateSeat('L1-A1', sector, {x:2, y: 2}, sample1);
  stadium.CreateSeat('L1-A1', sector, {x:5, y: 2}, sample2);
  stadium.CreateSeat('L1-A1', sector, {x:8, y: 2}, sample1);
  stadium.CreateSeat('L1-A1', sector, {x:11, y: 2}, sample2);
  stadium.CreateSeat('L1-A1', sector, {x:2, y: 6}, sample1);
}
